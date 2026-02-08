#!/usr/bin/env python3
"""Validate Krimi-Dinner case consistency for clues and cross-file references."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("ERROR CASE-000 - PyYAML fehlt. Bitte 'pip install pyyaml' ausfuehren.", file=sys.stderr)
    raise SystemExit(2) from exc


SEVERITY_ORDER = {"ERROR": 0, "WARN": 1}
HOLDER_ROLE_RE = re.compile(r"^role:(?P<id>[A-Za-z0-9_]+)$")
HOLDER_LOCATION_RE = re.compile(r"^location:(?P<id>[A-Za-z0-9_]+)$")

DEFAULT_CONFIG = {
    "min_clues_per_motive": 2,
    "min_incriminating_per_suspect": 1,
    "min_non_incriminating_per_suspect": 1,
    "beat_cluster_ratio_warn": 0.35,
    "exact_beat_overlap_warn_count": 3,
    "max_suspects_per_clue": 2,
    "max_motives_per_clue": 2,
    "max_targets_total_per_clue": 3,
    "testimony_hard_conclusion_keywords": [
        "beweist",
        "eindeutig",
        "sicher",
        "zweifelsfrei",
        "definitiv",
        "ohne zweifel",
    ],
    "testimony_warn_max_reliability": 2,
    "results_output_path": "reports/validate_case_results.txt",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    entity: str
    message: str


class Validator:
    def __init__(self, story_dir: Path, config: dict[str, Any]):
        self.story_dir = story_dir
        self.config = {**DEFAULT_CONFIG, **config}
        self.findings: list[Finding] = []
        self.files: dict[str, Any] = {}

    def add(self, severity: str, rule_id: str, entity: str, message: str) -> None:
        self.findings.append(Finding(severity=severity, rule_id=rule_id, entity=entity, message=message))

    def load_yaml(self, filename: str) -> dict[str, Any] | None:
        path = self.story_dir / filename
        if not path.exists():
            self.add("ERROR", "CASE-001", filename, f"Datei fehlt: {path}")
            return None
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if data is None:
            return {}
        if not isinstance(data, dict):
            self.add("ERROR", "CASE-002", filename, "Top-Level muss ein Mapping/Object sein.")
            return None
        return data

    @staticmethod
    def _get_list(value: Any) -> list[Any]:
        if value is None:
            return []
        return value if isinstance(value, list) else []

    def _load_required_data(self) -> dict[str, Any]:
        characters_doc = self.load_yaml("character.yaml") or {}
        locations_doc = self.load_yaml("locations.yaml") or {}
        motives_doc = self.load_yaml("motives.yaml") or {}
        clues_doc = self.load_yaml("clues.yaml") or {}
        timeline_doc = self.load_yaml("timeline.yaml") or {}

        timeline_root = timeline_doc.get("timeline", {})
        if timeline_doc and not isinstance(timeline_root, dict):
            self.add("ERROR", "CASE-003", "timeline.yaml", "Schluessel 'timeline' muss ein Mapping sein.")
            timeline_root = {}

        return {
            "characters": self._get_list(characters_doc.get("characters")),
            "locations": self._get_list(locations_doc.get("locations")),
            "motives": self._get_list(motives_doc.get("motives")),
            "clues": self._get_list(clues_doc.get("clues")),
            "beats": self._get_list(timeline_root.get("beats")),
        }

    def validate(self) -> list[Finding]:
        data = self._load_required_data()

        character_ids = {c.get("id") for c in data["characters"] if isinstance(c, dict) and c.get("id")}
        location_ids = {l.get("id") for l in data["locations"] if isinstance(l, dict) and l.get("id")}
        motive_ids = {m.get("id") for m in data["motives"] if isinstance(m, dict) and m.get("id")}
        beat_ids = {b.get("id") for b in data["beats"] if isinstance(b, dict) and b.get("id")}

        playable_character_ids = {cid for cid in character_ids if not str(cid).startswith("C_O_")}
        clue_ids = []
        motive_ref_counter: Counter[str] = Counter()
        suspect_polarity_counter: dict[str, Counter[str]] = defaultdict(Counter)
        beat_ref_counter: Counter[str] = Counter()
        beat_set_counter: Counter[tuple[str, ...]] = Counter()

        for index, clue in enumerate(data["clues"], start=1):
            if not isinstance(clue, dict):
                self.add("ERROR", "CLUE-000", f"clues[{index}]", "Clue-Eintrag muss ein Mapping sein.")
                continue

            clue_id = clue.get("id")
            entity = clue_id or f"clues[{index}]"
            if not clue_id:
                self.add("ERROR", "CLUE-000", entity, "Clue hat keine id.")
            else:
                clue_ids.append(clue_id)

            points_to = clue.get("points_to") if isinstance(clue.get("points_to"), dict) else {}
            suspects = self._get_list(points_to.get("suspects"))
            motives = self._get_list(points_to.get("motives"))

            for suspect_id in suspects:
                if suspect_id not in character_ids:
                    self.add(
                        "ERROR",
                        "CLUE-002",
                        entity,
                        f"points_to.suspects referenziert unbekannte Charakter-ID: {suspect_id}",
                    )

            for motive_id in motives:
                motive_ref_counter[motive_id] += 1
                if motive_id not in motive_ids:
                    self.add(
                        "ERROR",
                        "CLUE-003",
                        entity,
                        f"points_to.motives referenziert unbekannte Motiv-ID: {motive_id}",
                    )

            timeline_links = clue.get("timeline_links") if isinstance(clue.get("timeline_links"), dict) else {}
            related_beats = self._get_list(timeline_links.get("related_beats"))
            if not related_beats:
                self.add("ERROR", "CLUE-005", entity, "timeline_links.related_beats darf nicht leer sein.")
            for beat_id in related_beats:
                beat_ref_counter[beat_id] += 1
                if beat_id not in beat_ids:
                    self.add(
                        "ERROR",
                        "CLUE-004",
                        entity,
                        f"related_beats referenziert unbekannte Beat-ID: {beat_id}",
                    )
            if related_beats:
                beat_set_counter[tuple(sorted(set(str(b) for b in related_beats)))] += 1

            reliability = clue.get("reliability")
            if not isinstance(reliability, int) or reliability < 1 or reliability > 3:
                self.add("ERROR", "CLUE-006", entity, "reliability muss im Bereich 1..3 liegen.")

            discoverability = clue.get("discoverability") if isinstance(clue.get("discoverability"), dict) else {}
            earliest_round = discoverability.get("earliest_round")
            if not isinstance(earliest_round, int) or earliest_round < 1 or earliest_round > 4:
                self.add("ERROR", "CLUE-007", entity, "discoverability.earliest_round muss im Bereich 1..4 liegen.")

            holder = discoverability.get("holder")
            if not isinstance(holder, str):
                self.add(
                    "ERROR",
                    "CLUE-010",
                    entity,
                    "discoverability.holder muss gesetzt sein (GM | role:<id> | location:<id>).",
                )
            elif holder != "GM":
                role_match = HOLDER_ROLE_RE.match(holder)
                location_match = HOLDER_LOCATION_RE.match(holder)
                if role_match:
                    role_id = role_match.group("id")
                    if role_id not in character_ids:
                        self.add(
                            "ERROR",
                            "CLUE-010",
                            entity,
                            f"holder role referenziert unbekannte Charakter-ID: {role_id}",
                        )
                elif location_match:
                    location_id = location_match.group("id")
                    if location_id not in location_ids:
                        self.add(
                            "ERROR",
                            "CLUE-010",
                            entity,
                            f"holder location referenziert unbekannte Orts-ID: {location_id}",
                        )
                else:
                    self.add(
                        "ERROR",
                        "CLUE-010",
                        entity,
                        "holder-Format ungueltig. Erlaubt: GM, role:<CHAR_ID>, location:<LOC_ID>.",
                    )

            knowledge = clue.get("knowledge") if isinstance(clue.get("knowledge"), dict) else {}
            initial_holders = self._get_list(knowledge.get("initial_holders"))
            for holder_id in initial_holders:
                if holder_id not in character_ids:
                    self.add(
                        "ERROR",
                        "CLUE-008",
                        entity,
                        f"knowledge.initial_holders referenziert unbekannte Charakter-ID: {holder_id}",
                    )

            if not suspects and not motives:
                self.add(
                    "WARN",
                    "CLUE-020",
                    entity,
                    "Clue zeigt weder auf suspects noch motives (spielmechanisch ggf. zu lose).",
                )

            if len(set(suspects)) > int(self.config["max_suspects_per_clue"]):
                self.add(
                    "WARN",
                    "CLUE-023",
                    entity,
                    f"Zu viele Suspects ({len(set(suspects))}) fuer einen Clue.",
                )
            if len(set(motives)) > int(self.config["max_motives_per_clue"]):
                self.add(
                    "WARN",
                    "CLUE-023",
                    entity,
                    f"Zu viele Motive ({len(set(motives))}) fuer einen Clue.",
                )
            if len(set(suspects)) + len(set(motives)) > int(self.config["max_targets_total_per_clue"]):
                self.add(
                    "WARN",
                    "CLUE-023",
                    entity,
                    f"Zu viele Gesamtziele ({len(set(suspects)) + len(set(motives))}) fuer einen Clue.",
                )

            polarity = str(clue.get("polarity", "ambiguous")).strip().lower()
            if polarity not in {"incriminating", "exculpatory", "ambiguous"}:
                polarity = "ambiguous"
            for suspect_id in suspects:
                suspect_polarity_counter[suspect_id][polarity] += 1

            clue_type = str(clue.get("type", "")).strip().lower()
            if clue_type == "testimony":
                max_rel = int(self.config["testimony_warn_max_reliability"])
                if isinstance(reliability, int) and reliability <= max_rel:
                    text = f"{clue.get('title', '')} {clue.get('description', '')}".lower()
                    for keyword in self._get_list(self.config.get("testimony_hard_conclusion_keywords")):
                        if keyword and str(keyword).lower() in text:
                            self.add(
                                "WARN",
                                "CLUE-024",
                                entity,
                                "Testimony mit niedriger/mittlerer reliability enthaelt sehr harte Schlussfolgerung.",
                            )
                            break

        duplicate_clue_ids = [cid for cid, count in Counter(clue_ids).items() if count > 1]
        for cid in duplicate_clue_ids:
            self.add("ERROR", "CLUE-001", str(cid), "Clue-ID ist nicht eindeutig.")

        min_clues_per_motive = int(self.config["min_clues_per_motive"])
        for motive_id in sorted(motive_ids):
            if motive_ref_counter[motive_id] < min_clues_per_motive:
                self.add(
                    "ERROR",
                    "CLUE-009",
                    motive_id,
                    f"Motiv wird nur von {motive_ref_counter[motive_id]} Clues referenziert (mindestens {min_clues_per_motive} noetig).",
                )

        total_clues = len(data["clues"])
        if total_clues > 0:
            min_incr = int(self.config["min_incriminating_per_suspect"])
            min_non_incr = int(self.config["min_non_incriminating_per_suspect"])
            for suspect_id in sorted(playable_character_ids):
                counts = suspect_polarity_counter[suspect_id]
                if counts["incriminating"] < min_incr:
                    self.add(
                        "WARN",
                        "CLUE-021",
                        suspect_id,
                        f"Zu wenige belastende Clues ({counts['incriminating']}, erwartet mindestens {min_incr}).",
                    )
                non_incr = counts["exculpatory"] + counts["ambiguous"]
                if non_incr < min_non_incr:
                    self.add(
                        "WARN",
                        "CLUE-021",
                        suspect_id,
                        f"Zu wenige entlastende/ambivalente Clues ({non_incr}, erwartet mindestens {min_non_incr}).",
                    )

        if total_clues > 0:
            ratio_warn = float(self.config["beat_cluster_ratio_warn"])
            for beat_id, count in beat_ref_counter.items():
                ratio = count / total_clues
                if ratio > ratio_warn:
                    self.add(
                        "WARN",
                        "CLUE-022",
                        str(beat_id),
                        f"Beat wird von {count}/{total_clues} Clues referenziert ({ratio:.0%}) und ist ggf. ueberladen.",
                    )

            overlap_warn_count = int(self.config["exact_beat_overlap_warn_count"])
            for beat_set, count in beat_set_counter.items():
                if count >= overlap_warn_count and beat_set:
                    self.add(
                        "WARN",
                        "CLUE-022",
                        ",".join(beat_set),
                        f"{count} Clues referenzieren exakt dieselbe Beat-Kombination.",
                    )

        self.findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 99), f.rule_id, f.entity))
        return self.findings


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_story_dir = script_dir.parent / "story"
    default_config_path = script_dir / "validation_config.yaml"

    parser = argparse.ArgumentParser(description="Validate clue consistency for Krimi-Dinner data.")
    parser.add_argument("--story-dir", type=Path, default=default_story_dir, help="Pfad zu story/ (default: <repo>/story).")
    parser.add_argument("--config", type=Path, default=default_config_path, help="Pfad zur Validator-Config (YAML).")
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        print(f"WARN CASE-004 {config_path} - Config wird ignoriert (kein Mapping).", file=sys.stderr)
        return {}
    return raw


def build_output_lines(findings: list[Finding], generated_at: str) -> tuple[list[str], int, int]:
    lines: list[str] = [f"Generated at: {generated_at}", ""]
    for finding in findings:
        lines.append(f"{finding.severity} {finding.rule_id} {finding.entity} - {finding.message}")

    error_count = sum(1 for finding in findings if finding.severity == "ERROR")
    warn_count = sum(1 for finding in findings if finding.severity == "WARN")
    lines.append("")
    lines.append(f"Summary: {error_count} ERROR, {warn_count} WARN")
    return lines, error_count, warn_count


def build_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def resolve_output_path(raw_path: Any, story_dir: Path) -> Path | None:
    if raw_path is None:
        return None
    output_value = str(raw_path).strip()
    if output_value == "":
        return None
    output_path = Path(output_value)
    if not output_path.is_absolute():
        output_path = story_dir / output_path
    return output_path


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    validator = Validator(story_dir=args.story_dir, config=config)
    findings = validator.validate()

    generated_at = build_timestamp()
    lines, error_count, _ = build_output_lines(findings, generated_at)
    print("\n".join(lines))

    output_path = resolve_output_path(config.get("results_output_path"), args.story_dir)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {output_path}")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
