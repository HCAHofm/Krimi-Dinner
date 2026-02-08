# AGENTS Instructions

## Vorgehen bei jeder Aufgabe
* Bei jeder Aufgabe verpflichtend diese Referenzdateien prüfen: `docs/requirements/constraints.md`
* Einheitliche Referenzierung in allen Markdown-Dateien verwenden: `【F:pfad/zur/datei.md】`; wenn für eine konkrete Aussage nötig, optional präzisieren mit Zeilenbereich `【F:pfad/zur/datei.md†Lx-Ly】`.

## Hinweise für Erstellung von Krimi-Dinner Spiel
* Es wird nur in Dateien unter `/story/` geschrieben oder welche erstellt.


## Schritte für Erstellung von Krimi-Dinner Spiel
1. Grundsätzliche Story erstellen inkl Vorgeschichte. Mach dazu 10 Vorschläge mit Stichpunkten zum Inhalt der Geschichte.
2. Story wurde von Autor ausgewählt. Geschichte wird von dir detailliert ausformuliert und in `/story/storyline` abgelegt. Hier müssen Namen für Charaktere vergeben werden.
3. Schauplätze des Spiels werden nach der Struktur von `templates/locations.yaml` und basierend auf `/story/storyline` erstellt und unter `/story/locations.yaml` abgelegt.
4. Charaktere werden nach Vorgaben in `docs/requirements/constraints.md`, `/story/storyline`, `/story/locations.yaml` kreiert und in `story/character.yaml` abgelegt.
5. Die Motive der Charaktere werden nach der Struktur von `templates/motives.yaml` und basierend auf `/story/storyline`, `story/character.yaml` und `story/locations.yaml` erstellt und unter `/story/motives.yaml` abgelegt. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
6. Hinweise werden nach der Struktur von `templates/clues.yaml` und basierend auf `/story/storyline`, `story/character.yaml`, `story/locations.yaml` und `story/motives.yaml` erstellt und unter `/story/clues.yaml` abgelegt. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
7. Der zeitliche Ablauf rund um den Mord wird nach der Struktur `templates/timeline.yaml` und basierend auf `/story/storyline`, `story/character.yaml`, `story/locations.yaml`, `story/motives.yaml` und `story/clues.yaml` erstellt und unter `/story/timeline.yaml` abgelegt. Die in `story/clues.yaml` referenzierten `timeline_links.related_beats` müssen in `story/timeline.yaml` als `beats.id` konsistent auflösbar sein. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.

8. Überarbeiten von `/story/storyline` anhand der Infos aus `story/character.yaml`, `story/timeline.yaml`, `story/motives.yaml` und `story/clues.yaml`, sodass die Story konsistent und ausführlich ist.
