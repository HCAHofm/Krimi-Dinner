# Review zu `story/storyline`

## Formale Prüfung
- Referenzpflicht geprüft gegen `docs/requirements/constraints.md`【F:docs/requirements/constraints.md】.
- Template-Prüfung gegen `templates/story-description.md`: Datei ist aktuell leer (0 Byte), daher sind dort keine Keys/Abschnitte definiert, gegen die validiert werden kann.【F:templates/story-description.md】
- Prüfung der Muss-Inhalte aus den Constraints erfolgreich:
  - Setting vorhanden.
  - Opfer vorhanden.
  - Genau 4 verdächtige Rollen vorhanden (Charakter A, B, C, Mörder).
  - Kerntat mit Tatort, Tatzeitfenster und Anlass vorhanden.
  - 6-Akt-Struktur vorhanden.
  - Keine harten Referenzen auf nicht existierende Struktur-IDs (`M_*`, `K_*`, `B_*`, `L_*`).
  - Pro verdächtiger Rolle sind Motiv, belastbares Geheimnis und Gelegenheit enthalten.
  - Kein gemeinsames Essen als Story-Element im Ablauf.

## Logikprüfung
- Vorgeschichte, Erpressung und Tatanlass sind konsistent miteinander.
- Tatzeitfenster während Stromausfall ist plausibel und schafft Gelegenheit für mehrere Verdächtige.
- Alle vier Verdächtigen haben nachvollziehbare Risiken bei Offenlegung der Unfallwahrheit.
- Täterauflösung ist mit Motiv und Gelegenheit stimmig.

## Festgestellte harte Fehler
- Keine harten Fehler festgestellt, daher keine Korrektur in `story/storyline` notwendig.

## Hinweise für Folgeschritte
- In Schritt 3 sollten Orte so modelliert werden, dass das Tatfenster (Arbeitsraum/Verbindungsgang/Technikraum/Aufenthaltsraum) sauber abbildbar ist.
- In Schritt 4-7 müssen Alibis, Motive, Hinweise und Timeline streng gegen diese Storyline konsistent gehalten werden.【F:docs/requirements/constraints.md】

