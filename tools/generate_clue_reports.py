#!/usr/bin/env python3
"""Generate human-readable clue overview reports for Krimi-Dinner cases."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("ERROR REPORT-000 - PyYAML fehlt. Bitte 'pip install pyyaml' ausfuehren.", file=sys.stderr)
    raise SystemExit(2) from exc


HOLDER_ROLE_RE = re.compile(r"^role:(?P<id>[A-Za-z0-9_]+)$")
HOLDER_LOCATION_RE = re.compile(r"^location:(?P<id>[A-Za-z0-9_]+)$")
POLARITY_ORDER = {"incriminating": 0, "exculpatory": 1, "ambiguous": 2}
POLARITY_LABEL = {
    "incriminating": "belastend",
    "exculpatory": "entlastend",
    "ambiguous": "ambivalent",
}

DEFAULT_CONFIG: dict[str, Any] = {
    "story_dir": "../story",
    "inputs": {
        "characters": "character.yaml",
        "motives": "motives.yaml",
        "clues": "clues.yaml",
        "locations": "locations.yaml",
        "timeline": "timeline.yaml",
    },
    "output_dir": "reports",
    "outputs": {
        "clues_by_beat": "clues_by_beat.md",
        "clues_by_motive": "clues_by_motive.md",
        "clues_by_suspect": "clues_by_suspect.md",
        "dangling_refs": "dangling_refs.md",
        "coverage_summary": "coverage_summary.md",
    },
    "id_rules": {
        "victim_prefix": "C_O_",
    },
    "coverage_thresholds": {
        "min_clues_per_motive": 2,
        "min_incriminating_per_suspect": 1,
        "min_non_incriminating_per_suspect": 1,
        "beat_cluster_ratio_warn": 0.35,
    },
    "render": {
        "max_summary_points_per_clue": 3,
        "include_source_refs": True,
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else []


def norm_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def parse_hhmm(value: str) -> tuple[int, int]:
    try:
        hours, minutes = value.split(":")
        return int(hours), int(minutes)
    except (ValueError, AttributeError):
        return (99, 99)


def load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Datei fehlt: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Top-Level muss Mapping sein: {path}")
    return data


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        cleaned = [cell.replace("\n", "<br>") for cell in row]
        lines.append("| " + " | ".join(cleaned) + " |")
    return lines


class ClueReportGenerator:
    def __init__(self, story_dir: Path, config: dict[str, Any]):
        self.story_dir = story_dir
        self.config = config
        self.generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

        inputs = config.get("inputs", {})
        self.characters_path = self._resolve_story_path(inputs.get("characters", "character.yaml"))
        self.motives_path = self._resolve_story_path(inputs.get("motives", "motives.yaml"))
        self.clues_path = self._resolve_story_path(inputs.get("clues", "clues.yaml"))
        self.locations_path = self._resolve_story_path(inputs.get("locations", "locations.yaml"))
        self.timeline_path = self._resolve_story_path(inputs.get("timeline", "timeline.yaml"))

        self.characters_doc = load_yaml_file(self.characters_path)
        self.motives_doc = load_yaml_file(self.motives_path)
        self.clues_doc = load_yaml_file(self.clues_path)
        self.locations_doc = load_yaml_file(self.locations_path)
        self.timeline_doc = load_yaml_file(self.timeline_path)

        self.characters = [c for c in as_list(self.characters_doc.get("characters")) if isinstance(c, dict)]
        self.motives = [m for m in as_list(self.motives_doc.get("motives")) if isinstance(m, dict)]
        self.clues = [c for c in as_list(self.clues_doc.get("clues")) if isinstance(c, dict)]
        self.locations = [loc for loc in as_list(self.locations_doc.get("locations")) if isinstance(loc, dict)]
        timeline_root = self.timeline_doc.get("timeline")
        timeline_root = timeline_root if isinstance(timeline_root, dict) else {}
        self.beats = [b for b in as_list(timeline_root.get("beats")) if isinstance(b, dict)]
        self.timeline_meta_locations = {
            norm_text(loc_id)
            for loc_id in as_list(timeline_root.get("meta", {}).get("locations") if isinstance(timeline_root.get("meta"), dict) else [])
            if norm_text(loc_id)
        }

        self.character_by_id = {norm_text(c.get("id")): c for c in self.characters if norm_text(c.get("id"))}
        self.motive_by_id = {norm_text(m.get("id")): m for m in self.motives if norm_text(m.get("id"))}
        self.beat_by_id = {norm_text(b.get("id")): b for b in self.beats if norm_text(b.get("id"))}
        self.location_ids = {
            norm_text(location.get("id"))
            for location in self.locations
            if norm_text(location.get("id"))
        }
        self.location_ids.update(self.timeline_meta_locations)
        self.location_ids.update(norm_text(beat.get("location")) for beat in self.beats if norm_text(beat.get("location")))

        victim_prefix = norm_text(config.get("id_rules", {}).get("victim_prefix", "C_O_"))
        self.playable_character_ids = sorted(
            [cid for cid in self.character_by_id if not cid.startswith(victim_prefix)],
            key=self._character_sort_key,
        )

        self.clue_ids = [norm_text(clue.get("id")) for clue in self.clues if norm_text(clue.get("id"))]
        self.duplicate_clue_ids = sorted([cid for cid, count in Counter(self.clue_ids).items() if count > 1])

        self.clues_by_beat: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.clues_by_motive: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.clues_by_suspect: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._index_clues()

    def _resolve_story_path(self, raw_path: Any) -> Path:
        path = Path(norm_text(raw_path))
        if path.is_absolute():
            return path
        return self.story_dir / path

    def _character_sort_key(self, character_id: str) -> tuple[str, str]:
        character = self.character_by_id.get(character_id, {})
        return (norm_text(character.get("name")).lower(), character_id)

    def _motive_sort_key(self, motive_id: str) -> tuple[str, str]:
        motive = self.motive_by_id.get(motive_id, {})
        character_id = norm_text(motive.get("character"))
        return (self._character_sort_key(character_id)[0], motive_id)

    def _beat_sort_key(self, beat_id: str) -> tuple[tuple[int, int], str]:
        beat = self.beat_by_id.get(beat_id, {})
        return (parse_hhmm(norm_text(beat.get("time"))), beat_id)

    def _clue_sort_key(self, clue: dict[str, Any]) -> tuple[int, int, str]:
        discoverability = clue.get("discoverability")
        discoverability = discoverability if isinstance(discoverability, dict) else {}
        round_value = discoverability.get("earliest_round")
        round_key = round_value if isinstance(round_value, int) else 99
        polarity = norm_text(clue.get("polarity")).lower()
        polarity_key = POLARITY_ORDER.get(polarity, 99)
        return (round_key, polarity_key, norm_text(clue.get("id")))

    def _index_clues(self) -> None:
        for clue in self.clues:
            points_to = clue.get("points_to")
            points_to = points_to if isinstance(points_to, dict) else {}
            suspects = sorted(set(norm_text(s) for s in as_list(points_to.get("suspects")) if norm_text(s)))
            motives = sorted(set(norm_text(m) for m in as_list(points_to.get("motives")) if norm_text(m)))

            timeline_links = clue.get("timeline_links")
            timeline_links = timeline_links if isinstance(timeline_links, dict) else {}
            beats = sorted(set(norm_text(b) for b in as_list(timeline_links.get("related_beats")) if norm_text(b)))

            for suspect_id in suspects:
                self.clues_by_suspect[suspect_id].append(clue)
            for motive_id in motives:
                self.clues_by_motive[motive_id].append(clue)
            for beat_id in beats:
                self.clues_by_beat[beat_id].append(clue)

    def _format_character(self, character_id: str) -> str:
        character = self.character_by_id.get(character_id)
        if not character:
            return f"`{character_id}`"
        name = norm_text(character.get("name"))
        return f"{name} (`{character_id}`)"

    def _format_motive(self, motive_id: str) -> str:
        motive = self.motive_by_id.get(motive_id)
        if not motive:
            return f"`{motive_id}`"
        character_id = norm_text(motive.get("character"))
        murder_flag = " (moerderisch)" if motive.get("murder") is True else ""
        return f"`{motive_id}`{murder_flag} - {self._format_character(character_id)}"

    def _format_beat(self, beat_id: str) -> str:
        beat = self.beat_by_id.get(beat_id)
        if not beat:
            return f"`{beat_id}`"
        time = norm_text(beat.get("time"))
        location = norm_text(beat.get("location"))
        return f"`{beat_id}` ({time}, `{location}`)"

    def _clue_summary(self, clue: dict[str, Any]) -> str:
        max_points = int(self.config.get("render", {}).get("max_summary_points_per_clue", 3))
        summary_points = [norm_text(p) for p in as_list(clue.get("summary_points")) if norm_text(p)]
        if not summary_points:
            return "-"
        return "; ".join(summary_points[:max_points])

    def _clue_row(self, clue: dict[str, Any], include_summary: bool = False) -> list[str]:
        clue_id = norm_text(clue.get("id")) or "(ohne-id)"
        title = norm_text(clue.get("title"))
        clue_type = norm_text(clue.get("type")) or "-"
        polarity = norm_text(clue.get("polarity")).lower()
        reliability = clue.get("reliability")
        discoverability = clue.get("discoverability")
        discoverability = discoverability if isinstance(discoverability, dict) else {}
        round_value = discoverability.get("earliest_round")
        round_label = str(round_value) if isinstance(round_value, int) else "-"

        points_to = clue.get("points_to")
        points_to = points_to if isinstance(points_to, dict) else {}
        suspect_labels = [self._format_character(sid) for sid in as_list(points_to.get("suspects")) if norm_text(sid)]
        motive_labels = [self._format_motive(mid) for mid in as_list(points_to.get("motives")) if norm_text(mid)]

        timeline_links = clue.get("timeline_links")
        timeline_links = timeline_links if isinstance(timeline_links, dict) else {}
        beat_labels = [self._format_beat(bid) for bid in as_list(timeline_links.get("related_beats")) if norm_text(bid)]

        row = [
            f"`{clue_id}` - {title}",
            round_label,
            POLARITY_LABEL.get(polarity, polarity or "-"),
            clue_type,
            str(reliability) if isinstance(reliability, int) else "-",
            ", ".join(suspect_labels) if suspect_labels else "-",
            ", ".join(motive_labels) if motive_labels else "-",
            ", ".join(beat_labels) if beat_labels else "-",
        ]
        if include_summary:
            row.append(self._clue_summary(clue))
        return row

    def _build_report_header(self, title: str) -> list[str]:
        lines = [f"# {title}", ""]
        lines.append(f"Generiert am: `{self.generated_at}`")
        if self.config.get("render", {}).get("include_source_refs", True):
            lines.append(
                "Quellen: "
                "【F:story/clues.yaml】, "
                "【F:story/motives.yaml】, "
                "【F:story/character.yaml】, "
                "【F:story/locations.yaml】, "
                "【F:story/timeline.yaml】"
            )
        lines.append("")
        return lines

    def _write_report(self, output_path: Path, lines: list[str]) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    def _collect_dangling_refs(self) -> dict[str, list[list[str]]]:
        unknown_suspects: list[list[str]] = []
        unknown_motives: list[list[str]] = []
        unknown_beats: list[list[str]] = []
        unknown_holder_roles: list[list[str]] = []
        unknown_holder_locations: list[list[str]] = []
        invalid_holder_format: list[list[str]] = []
        unknown_initial_holders: list[list[str]] = []
        unknown_motive_characters: list[list[str]] = []
        unknown_motive_clues: list[list[str]] = []

        known_clue_ids = set(self.clue_ids)

        for clue in self.clues:
            clue_id = norm_text(clue.get("id")) or "(ohne-id)"

            points_to = clue.get("points_to")
            points_to = points_to if isinstance(points_to, dict) else {}
            for suspect_id in as_list(points_to.get("suspects")):
                suspect_id = norm_text(suspect_id)
                if suspect_id and suspect_id not in self.character_by_id:
                    unknown_suspects.append([f"`{clue_id}`", f"`{suspect_id}`"])

            for motive_id in as_list(points_to.get("motives")):
                motive_id = norm_text(motive_id)
                if motive_id and motive_id not in self.motive_by_id:
                    unknown_motives.append([f"`{clue_id}`", f"`{motive_id}`"])

            timeline_links = clue.get("timeline_links")
            timeline_links = timeline_links if isinstance(timeline_links, dict) else {}
            for beat_id in as_list(timeline_links.get("related_beats")):
                beat_id = norm_text(beat_id)
                if beat_id and beat_id not in self.beat_by_id:
                    unknown_beats.append([f"`{clue_id}`", f"`{beat_id}`"])

            discoverability = clue.get("discoverability")
            discoverability = discoverability if isinstance(discoverability, dict) else {}
            holder = norm_text(discoverability.get("holder"))
            if holder and holder != "GM":
                role_match = HOLDER_ROLE_RE.match(holder)
                location_match = HOLDER_LOCATION_RE.match(holder)
                if role_match:
                    role_id = role_match.group("id")
                    if role_id not in self.character_by_id:
                        unknown_holder_roles.append([f"`{clue_id}`", f"`{holder}`"])
                elif location_match:
                    location_id = location_match.group("id")
                    if location_id not in self.location_ids:
                        unknown_holder_locations.append([f"`{clue_id}`", f"`{holder}`"])
                else:
                    invalid_holder_format.append([f"`{clue_id}`", f"`{holder}`"])

            knowledge = clue.get("knowledge")
            knowledge = knowledge if isinstance(knowledge, dict) else {}
            for holder_id in as_list(knowledge.get("initial_holders")):
                holder_id = norm_text(holder_id)
                if holder_id and holder_id not in self.character_by_id:
                    unknown_initial_holders.append([f"`{clue_id}`", f"`{holder_id}`"])

        for motive in self.motives:
            motive_id = norm_text(motive.get("id")) or "(ohne-id)"
            character_id = norm_text(motive.get("character"))
            if character_id and character_id not in self.character_by_id:
                unknown_motive_characters.append([f"`{motive_id}`", f"`{character_id}`"])

            clue_support = motive.get("clue_support")
            clue_support = clue_support if isinstance(clue_support, dict) else {}
            for section in ("primary", "secondary"):
                for item in as_list(clue_support.get(section)):
                    if not isinstance(item, dict):
                        continue
                    clue_ref = norm_text(item.get("clue_id"))
                    if clue_ref and clue_ref not in known_clue_ids:
                        unknown_motive_clues.append([f"`{motive_id}`", section, f"`{clue_ref}`"])

            for item in as_list(motive.get("counter_clues")):
                if not isinstance(item, dict):
                    continue
                clue_ref = norm_text(item.get("clue_id"))
                if clue_ref and clue_ref not in known_clue_ids:
                    unknown_motive_clues.append([f"`{motive_id}`", "counter_clues", f"`{clue_ref}`"])

        duplicates = [[f"`{cid}`", "mehrfach vorhanden"] for cid in self.duplicate_clue_ids]

        return {
            "duplicate_clue_ids": duplicates,
            "unknown_suspects": unknown_suspects,
            "unknown_motives": unknown_motives,
            "unknown_beats": unknown_beats,
            "unknown_holder_roles": unknown_holder_roles,
            "unknown_holder_locations": unknown_holder_locations,
            "invalid_holder_format": invalid_holder_format,
            "unknown_initial_holders": unknown_initial_holders,
            "unknown_motive_characters": unknown_motive_characters,
            "unknown_motive_clues": unknown_motive_clues,
        }

    def build_clues_by_beat(self) -> list[str]:
        lines = self._build_report_header("Clues Nach Beat")
        all_beat_ids = sorted(self.beat_by_id.keys(), key=self._beat_sort_key)

        for beat_id in all_beat_ids:
            beat = self.beat_by_id.get(beat_id, {})
            time = norm_text(beat.get("time")) or "--:--"
            location = norm_text(beat.get("location")) or "-"
            visibility = norm_text(beat.get("visibility")) or "-"
            description = norm_text(beat.get("description"))
            lines.append(f"## {time} - `{beat_id}`")
            lines.append(f"Ort: `{location}` | Sichtbarkeit: `{visibility}`")
            if description:
                lines.append(f"Beat: {description}")
            lines.append("")

            related = sorted(self.clues_by_beat.get(beat_id, []), key=self._clue_sort_key)
            if not related:
                lines.append("_Keine Clues referenzieren diesen Beat._")
                lines.append("")
                continue

            rows = [self._clue_row(clue, include_summary=True) for clue in related]
            lines.extend(
                markdown_table(
                    ["Clue", "Runde", "Polarity", "Typ", "Rel", "Suspects", "Motive", "Beats", "Kurzfassung"],
                    rows,
                )
            )
            lines.append("")

        unknown_beats = sorted([bid for bid in self.clues_by_beat if bid not in self.beat_by_id])
        lines.append("## Clues Mit Unbekannten Beat-IDs")
        lines.append("")
        if not unknown_beats:
            lines.append("_Keine unbekannten Beat-Referenzen gefunden._")
            lines.append("")
        else:
            for beat_id in unknown_beats:
                lines.append(f"### `{beat_id}`")
                rows = [self._clue_row(clue) for clue in sorted(self.clues_by_beat[beat_id], key=self._clue_sort_key)]
                lines.extend(markdown_table(["Clue", "Runde", "Polarity", "Typ", "Rel", "Suspects", "Motive", "Beats"], rows))
                lines.append("")

        return lines

    def build_clues_by_motive(self) -> list[str]:
        lines = self._build_report_header("Clues Nach Motiv")
        motive_ids = sorted(self.motive_by_id.keys(), key=self._motive_sort_key)

        for motive_id in motive_ids:
            motive = self.motive_by_id[motive_id]
            character_id = norm_text(motive.get("character"))
            strength = motive.get("strength")
            murder = motive.get("murder")
            description = norm_text(motive.get("description"))

            lines.append(f"## `{motive_id}`")
            lines.append(f"Charakter: {self._format_character(character_id)}")
            lines.append(f"Staerke: `{strength}` | murder: `{murder}`")
            if description:
                lines.append(f"Beschreibung: {description}")
            lines.append("")

            declared_rows: list[list[str]] = []
            clue_support = motive.get("clue_support")
            clue_support = clue_support if isinstance(clue_support, dict) else {}
            for section in ("primary", "secondary"):
                for item in as_list(clue_support.get(section)):
                    if not isinstance(item, dict):
                        continue
                    clue_id = norm_text(item.get("clue_id"))
                    why = norm_text(item.get("why"))
                    exists = "ja" if clue_id in self.clue_ids else "nein"
                    linked = "ja" if any(norm_text(c.get("id")) == clue_id for c in self.clues_by_motive.get(motive_id, [])) else "nein"
                    declared_rows.append([section, f"`{clue_id}`", exists, linked, why or "-"])
            for item in as_list(motive.get("counter_clues")):
                if not isinstance(item, dict):
                    continue
                clue_id = norm_text(item.get("clue_id"))
                why = norm_text(item.get("why"))
                exists = "ja" if clue_id in self.clue_ids else "nein"
                linked = "ja" if any(norm_text(c.get("id")) == clue_id for c in self.clues_by_motive.get(motive_id, [])) else "nein"
                declared_rows.append(["counter_clues", f"`{clue_id}`", exists, linked, why or "-"])

            lines.append("### Referenzen In `motives.yaml`")
            lines.append("")
            if declared_rows:
                lines.extend(markdown_table(["Bereich", "Clue-ID", "Existiert", "Verlinkt auf Motiv", "Notiz"], declared_rows))
            else:
                lines.append("_Keine expliziten Clue-Referenzen im Motiv eingetragen._")
            lines.append("")

            linked_clues = sorted(self.clues_by_motive.get(motive_id, []), key=self._clue_sort_key)
            lines.append("### Clues Mit `points_to.motives`")
            lines.append("")
            if linked_clues:
                rows = [self._clue_row(clue, include_summary=True) for clue in linked_clues]
                lines.extend(
                    markdown_table(
                        ["Clue", "Runde", "Polarity", "Typ", "Rel", "Suspects", "Motive", "Beats", "Kurzfassung"],
                        rows,
                    )
                )
            else:
                lines.append("_Kein Clue verweist ueber `points_to.motives` auf dieses Motiv._")
            lines.append("")

        return lines

    def build_clues_by_suspect(self) -> list[str]:
        lines = self._build_report_header("Clues Nach Verdaechtigem")

        for suspect_id in self.playable_character_ids:
            lines.append(f"## {self._format_character(suspect_id)}")
            motive_ids = sorted(
                [mid for mid, motive in self.motive_by_id.items() if norm_text(motive.get("character")) == suspect_id],
                key=self._motive_sort_key,
            )
            lines.append(f"Motive: {', '.join(f'`{m}`' for m in motive_ids) if motive_ids else '-'}")
            lines.append("")

            related = sorted(self.clues_by_suspect.get(suspect_id, []), key=self._clue_sort_key)
            if not related:
                lines.append("_Keine Clues referenzieren diesen Verdaechtigen._")
                lines.append("")
                continue

            groups = {"incriminating": [], "exculpatory": [], "ambiguous": []}
            for clue in related:
                polarity = norm_text(clue.get("polarity")).lower()
                if polarity not in groups:
                    polarity = "ambiguous"
                groups[polarity].append(clue)

            for polarity in ("incriminating", "exculpatory", "ambiguous"):
                lines.append(f"### {POLARITY_LABEL[polarity].capitalize()}")
                lines.append("")
                clues_in_group = sorted(groups[polarity], key=self._clue_sort_key)
                if clues_in_group:
                    rows = [self._clue_row(clue, include_summary=True) for clue in clues_in_group]
                    lines.extend(
                        markdown_table(
                            ["Clue", "Runde", "Polarity", "Typ", "Rel", "Suspects", "Motive", "Beats", "Kurzfassung"],
                            rows,
                        )
                    )
                else:
                    lines.append("_Keine Clues in dieser Kategorie._")
                lines.append("")

        unknown_suspects = sorted([sid for sid in self.clues_by_suspect if sid not in self.character_by_id])
        lines.append("## Clues Mit Unbekannten Suspect-IDs")
        lines.append("")
        if not unknown_suspects:
            lines.append("_Keine unbekannten Suspect-Referenzen gefunden._")
            lines.append("")
        else:
            for suspect_id in unknown_suspects:
                lines.append(f"### `{suspect_id}`")
                rows = [self._clue_row(clue) for clue in sorted(self.clues_by_suspect[suspect_id], key=self._clue_sort_key)]
                lines.extend(markdown_table(["Clue", "Runde", "Polarity", "Typ", "Rel", "Suspects", "Motive", "Beats"], rows))
                lines.append("")

        return lines

    def build_dangling_refs(self) -> list[str]:
        lines = self._build_report_header("Dangling References")
        refs = self._collect_dangling_refs()

        def section(title: str, rows: list[list[str]], headers: list[str], empty_msg: str) -> None:
            lines.append(f"## {title}")
            lines.append("")
            if rows:
                lines.extend(markdown_table(headers, rows))
            else:
                lines.append(empty_msg)
            lines.append("")

        section(
            "Doppelte Clue-IDs",
            refs["duplicate_clue_ids"],
            ["Clue-ID", "Status"],
            "_Keine doppelten Clue-IDs gefunden._",
        )
        section(
            "Unbekannte `points_to.suspects`",
            refs["unknown_suspects"],
            ["Clue", "Unbekannte Suspect-ID"],
            "_Keine unbekannten Suspect-Referenzen gefunden._",
        )
        section(
            "Unbekannte `points_to.motives`",
            refs["unknown_motives"],
            ["Clue", "Unbekannte Motiv-ID"],
            "_Keine unbekannten Motiv-Referenzen gefunden._",
        )
        section(
            "Unbekannte `timeline_links.related_beats`",
            refs["unknown_beats"],
            ["Clue", "Unbekannte Beat-ID"],
            "_Keine unbekannten Beat-Referenzen gefunden._",
        )
        section(
            "Unbekannte Discoverability-Rollen",
            refs["unknown_holder_roles"],
            ["Clue", "holder"],
            "_Keine unbekannten Rollen in `discoverability.holder` gefunden._",
        )
        section(
            "Unbekannte Discoverability-Orte",
            refs["unknown_holder_locations"],
            ["Clue", "holder"],
            "_Keine unbekannten Orte in `discoverability.holder` gefunden._",
        )
        section(
            "Ungueltiges Discoverability-Format",
            refs["invalid_holder_format"],
            ["Clue", "holder"],
            "_Kein ungueltiges Holder-Format gefunden._",
        )
        section(
            "Unbekannte `knowledge.initial_holders`",
            refs["unknown_initial_holders"],
            ["Clue", "Unbekannte Charakter-ID"],
            "_Keine unbekannten `knowledge.initial_holders` gefunden._",
        )
        section(
            "Unbekannte Motiv-Charaktere",
            refs["unknown_motive_characters"],
            ["Motiv", "Unbekannte Charakter-ID"],
            "_Keine unbekannten Charakter-Referenzen in Motiven gefunden._",
        )
        section(
            "Unbekannte Clue-IDs in Motivreferenzen",
            refs["unknown_motive_clues"],
            ["Motiv", "Bereich", "Unbekannte Clue-ID"],
            "_Keine unbekannten Clue-Referenzen in Motiven gefunden._",
        )

        return lines

    def build_coverage_summary(self) -> list[str]:
        lines = self._build_report_header("Coverage Summary")
        thresholds = self.config.get("coverage_thresholds", {})
        min_clues_per_motive = int(thresholds.get("min_clues_per_motive", 2))
        min_incr = int(thresholds.get("min_incriminating_per_suspect", 1))
        min_non_incr = int(thresholds.get("min_non_incriminating_per_suspect", 1))
        beat_cluster_ratio_warn = float(thresholds.get("beat_cluster_ratio_warn", 0.35))

        total_clues = len(self.clues)
        lines.append("## Gesamt")
        lines.append("")
        lines.append(f"- Clues gesamt: **{total_clues}**")
        lines.append(f"- Beats gesamt: **{len(self.beats)}**")
        lines.append(f"- Motive gesamt: **{len(self.motives)}**")
        lines.append(f"- Spielbare Verdaechtige: **{len(self.playable_character_ids)}**")
        lines.append("")

        clue_type_counts = Counter(norm_text(clue.get("type")).lower() or "unknown" for clue in self.clues)
        lines.append("## Clues Pro Typ")
        lines.append("")
        type_rows = [[f"`{clue_type}`", str(count)] for clue_type, count in sorted(clue_type_counts.items())]
        lines.extend(markdown_table(["Typ", "Anzahl"], type_rows))
        lines.append("")

        polarity_counts = Counter(
            norm_text(clue.get("polarity")).lower() if norm_text(clue.get("polarity")).lower() in POLARITY_ORDER else "ambiguous"
            for clue in self.clues
        )
        lines.append("## Clues Pro Polarity")
        lines.append("")
        pol_rows = [[POLARITY_LABEL.get(p, p), str(polarity_counts.get(p, 0))] for p in ("incriminating", "exculpatory", "ambiguous")]
        lines.extend(markdown_table(["Polarity", "Anzahl"], pol_rows))
        lines.append("")

        lines.append("## Abdeckung Pro Motiv")
        lines.append("")
        motive_rows: list[list[str]] = []
        for motive_id in sorted(self.motive_by_id.keys(), key=self._motive_sort_key):
            motive = self.motive_by_id[motive_id]
            char_id = norm_text(motive.get("character"))
            count = len(self.clues_by_motive.get(motive_id, []))
            status = "ok" if count >= min_clues_per_motive else f"unter min ({min_clues_per_motive})"
            motive_rows.append(
                [
                    f"`{motive_id}`",
                    self._format_character(char_id),
                    str(count),
                    status,
                    "ja" if motive.get("murder") is True else "nein",
                ]
            )
        lines.extend(markdown_table(["Motiv", "Charakter", "Clues", "Status", "murder"], motive_rows))
        lines.append("")

        lines.append("## Abdeckung Pro Verdaechtigem")
        lines.append("")
        suspect_rows: list[list[str]] = []
        for suspect_id in self.playable_character_ids:
            related = self.clues_by_suspect.get(suspect_id, [])
            counts = Counter()
            for clue in related:
                polarity = norm_text(clue.get("polarity")).lower()
                if polarity not in {"incriminating", "exculpatory", "ambiguous"}:
                    polarity = "ambiguous"
                counts[polarity] += 1
            non_incr = counts["exculpatory"] + counts["ambiguous"]
            status_incr = "ok" if counts["incriminating"] >= min_incr else f"unter min ({min_incr})"
            status_non_incr = "ok" if non_incr >= min_non_incr else f"unter min ({min_non_incr})"
            suspect_rows.append(
                [
                    self._format_character(suspect_id),
                    str(counts["incriminating"]),
                    str(counts["exculpatory"]),
                    str(counts["ambiguous"]),
                    str(non_incr),
                    status_incr,
                    status_non_incr,
                ]
            )
        lines.extend(
            markdown_table(
                ["Verdaechtiger", "Belastend", "Entlastend", "Ambivalent", "Nicht-belastend", "Belastend-Status", "Nicht-belastend-Status"],
                suspect_rows,
            )
        )
        lines.append("")

        lines.append("## Abdeckung Pro Beat")
        lines.append("")
        beat_rows: list[list[str]] = []
        for beat_id in sorted(self.beat_by_id.keys(), key=self._beat_sort_key):
            beat = self.beat_by_id[beat_id]
            count = len(self.clues_by_beat.get(beat_id, []))
            ratio = (count / total_clues) if total_clues else 0.0
            status = "ok" if ratio <= beat_cluster_ratio_warn else f"ueber {beat_cluster_ratio_warn:.0%}"
            beat_rows.append(
                [
                    f"`{beat_id}`",
                    norm_text(beat.get("time")) or "-",
                    f"`{norm_text(beat.get('location'))}`",
                    str(count),
                    f"{ratio:.0%}",
                    status,
                ]
            )
        lines.extend(markdown_table(["Beat", "Zeit", "Ort", "Clues", "Anteil", "Status"], beat_rows))
        lines.append("")

        return lines

    def generate_reports(self, output_dir: Path) -> dict[str, Path]:
        outputs = self.config.get("outputs", {})
        rendered: dict[str, list[str]] = {
            "clues_by_beat": self.build_clues_by_beat(),
            "clues_by_motive": self.build_clues_by_motive(),
            "clues_by_suspect": self.build_clues_by_suspect(),
            "dangling_refs": self.build_dangling_refs(),
            "coverage_summary": self.build_coverage_summary(),
        }

        written_files: dict[str, Path] = {}
        for key, lines in rendered.items():
            raw_name = norm_text(outputs.get(key))
            if not raw_name:
                continue
            output_path = Path(raw_name)
            if not output_path.is_absolute():
                output_path = output_dir / output_path
            self._write_report(output_path, lines)
            written_files[key] = output_path
        return written_files


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Generate clue overview reports from story/*.yaml data.")
    parser.add_argument(
        "--config",
        type=Path,
        default=script_dir / "clue_reports_config.yaml",
        help="Pfad zur Report-Config (YAML).",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return dict(DEFAULT_CONFIG)
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        print(f"WARN REPORT-001 {config_path} - Config ist kein Mapping, Defaults werden genutzt.", file=sys.stderr)
        raw = {}
    return deep_merge(DEFAULT_CONFIG, raw)


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    config = load_config(config_path)

    config_base = config_path.parent
    story_dir_raw = norm_text(config.get("story_dir")) or "../story"
    story_dir = Path(story_dir_raw)
    if not story_dir.is_absolute():
        story_dir = (config_base / story_dir).resolve()

    output_dir_raw = norm_text(config.get("output_dir")) or "reports"
    output_dir = Path(output_dir_raw)
    if not output_dir.is_absolute():
        output_dir = (story_dir / output_dir).resolve()

    generator = ClueReportGenerator(story_dir=story_dir, config=config)
    written = generator.generate_reports(output_dir=output_dir)

    print(f"Generated at: {generator.generated_at}")
    for key, path in sorted(written.items()):
        print(f"{key}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
