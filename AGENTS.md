# AGENTS Instructions

## Vorgehen bei jeder Aufgabe
* Bei jeder Aufgabe verpflichtend diese Referenzdateien prüfen: `docs/requirements/constraints.md`
* Einheitliche Referenzierung in allen Markdown-Dateien verwenden: `【F:pfad/zur/datei.md】`; wenn für eine konkrete Aussage nötig, optional präzisieren mit Zeilenbereich `【F:pfad/zur/datei.md†Lx-Ly】`.

## Hinweise für Erstellung von Krimi-Dinner Spiel
* Es wird nur in Dateien unter `/story/` geschrieben oder welche erstellt.


## Schritte für Erstellung von Krimi-Dinner Spiel
1. Grundsätzliche Story erstellen inkl Vorgeschichte. Mach dazu 10 Vorschläge mit Stichpunkten zum Inhalt der Geschichte.
2. Story-Ausarbeitung und Prüfung
   - a) Story wurde von Autor ausgewählt. Geschichte wird detailliert ausformuliert und in `/story/storyline` abgelegt. Charakter bekommen die Namen Charakter A, B, C, Moerder und Opfer. Da dies vor den strukturierten Dateien erfolgt, dürfen in diesem Schritt keine harten Referenzen auf noch nicht existierende IDs aus `story/character.yaml`, `story/alibis.yaml`, `story/motives.yaml`, `story/clues.yaml` oder `story/timeline.yaml` vorausgesetzt werden.
   - b) Prüfe, ob die Datei `/story/storyline` alle im Template `templates/story-description.md` geforderten Keys/Abschnitte enthält und keine zusätzlichen erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/storyline_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/storyline`.
3. Schauplätze erstellen und prüfen
   - a) Schauplätze des Spiels werden nach der Struktur von `templates/locations.yaml` und basierend auf `/story/storyline` erstellt und unter `/story/locations.yaml` abgelegt.
   - b) Prüfe, ob die Datei `/story/locations.yaml` alle Keys aus `templates/locations.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/locations.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/locations.yaml`.
4. Charaktere erstellen und prüfen
   - a) Charaktere werden nach Vorgaben in `docs/requirements/constraints.md`, `/story/storyline`, `/story/locations.yaml` kreiert und in `story/character.yaml` abgelegt.
   - b) Prüfe, ob die Datei `/story/character.yaml` alle Keys aus `templates/characters.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/character.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/character.yaml`.
5. Motive erstellen und prüfen
   - a) Die Motive der Charaktere werden nach der Struktur von `templates/motives.yaml` und basierend auf `/story/storyline`, `story/character.yaml` und `story/locations.yaml` erstellt und unter `/story/motives.yaml` abgelegt. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
   - b) Prüfe, ob die Datei `/story/motives.yaml` alle Keys aus `templates/motives.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/motives.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/motives.yaml`.
6. Alibis erstellen und prüfen
   - a) Die Alibis der Charaktere werden nach der Struktur von `templates/alibis.yaml` und basierend auf `/story/storyline`, `story/character.yaml`, `story/locations.yaml` und `story/motives.yaml` erstellt und unter `/story/alibis.yaml` abgelegt. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
   - b) Prüfe, ob die Datei `/story/alibis.yaml` alle Keys aus `templates/alibis.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/alibis.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/alibis.yaml`.
7. Hinweise erstellen und prüfen
   - a) Hinweise werden nach der Struktur von `templates/clues.yaml` und basierend auf `/story/storyline`, `story/character.yaml`, `story/locations.yaml`, `story/alibis.yaml` und `story/motives.yaml` erstellt und unter `/story/clues.yaml` abgelegt. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
   - b) Prüfe, ob die Datei `/story/clues.yaml` alle Keys aus `templates/clues.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/clues.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/clues.yaml`.
8. Timeline erstellen und prüfen
   - a) Der zeitliche Ablauf rund um den Mord wird nach der Struktur `templates/timeline.yaml` und basierend auf `/story/storyline`, `story/character.yaml`, `story/locations.yaml`, `story/alibis.yaml`, `story/motives.yaml` und `story/clues.yaml` erstellt und unter `/story/timeline.yaml` abgelegt. Die in `story/clues.yaml` referenzierten `timeline_links.related_beats` müssen in `story/timeline.yaml` als `beats.id` konsistent auflösbar sein. Es MÜSSEN die Vorgaben in `docs/requirements/constraints.md` eingehalten werden.
   - b) Prüfe, ob die Datei `/story/timeline.yaml` alle Keys aus `templates/timeline.yaml` enthält und keine erfundenen Keys enthält. Prüfe zusätzlich auf Logikfehler und schreibe diese in `/story/timeline.yaml_review.md`. Wenn harte Fehler erkannt werden, korrigiere sie direkt in `/story/timeline.yaml`.

# Noch nicht klar ob das verändert wird. z.B. nutze validate modul um logikbrüche zu identifizieren
9. Überarbeiten von `/story/storyline` anhand der Infos aus `story/character.yaml`, `story/alibis.yaml`, `story/timeline.yaml`, `story/motives.yaml` und `story/clues.yaml`, sodass die Story konsistent und ausführlich ist.
10. Erstelle eine Übersicht der Clues für menschliche augen basierend auf `story/storyline`, `story/character.yaml`, `story/alibis.yaml`, `story/motives.yaml`, `story/clues.yaml` und `story/timeline.yaml`.
11. Erstelle das Spielmaterial basierend auf `story/storyline`, `story/locations.yaml`, `story/character.yaml`, `story/alibis.yaml`, `story/motives.yaml`, `story/clues.yaml` und `story/timeline.yaml`.
