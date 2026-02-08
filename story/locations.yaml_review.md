# Review zu `story/locations.yaml`

## Formale Prüfung
- Template-Prüfung gegen `templates/locations.yaml` durchgeführt.【F:templates/locations.yaml】
- Vorhandene Top-Level-Struktur korrekt: `locations`.
- Alle Einträge enthalten nur die geforderten Keys: `id`, `name`, `access`.
- Keine zusätzlichen erfundenen Keys gefunden.

## Logikprüfung gegen Storyline
- Orte decken die in der Storyline benötigten Kernbereiche ab: Aufenthaltsbereich, Tatort, Bewegungsachse im Nordflügel, Technikraum für Stromausfall-Kontext, Waffenzugang, private Zimmer.【F:story/storyline】
- Zugriffsstufen sind für spätere Alibi- und Gelegenheitsprüfung nutzbar (`alle`, `nur_personal`, `nur_mit_schluessel`).
- Tatort und potenzielle Täterbewegung sind räumlich plausibel modelliert.

## Festgestellte harte Fehler
- Keine harten Fehler festgestellt, daher keine Korrektur in `story/locations.yaml` notwendig.

## Hinweise für Folgeschritte
- In `story/character.yaml` sollten Alibis gezielt diese `location`-IDs referenzieren.
- In `story/timeline.yaml` muss das Tatzeitfenster auf diese Orts-IDs konsistent aufgelöst werden.【F:docs/requirements/constraints.md】

