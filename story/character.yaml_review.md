# Review zu `story/character.yaml`

## Formale Prüfung
- Referenzpflicht geprüft gegen die Muss-Kriterien.【F:docs/requirements/constraints.md】
- Struktur als `characters`-Liste entspricht dem Template-Stil.【F:templates/characters.yaml】
- Pflichtanzahl erfüllt: 4 spielbare Rollen (`C_A`, `C_B`, `C_C`, `C_MOERDER`) plus genau 1 Opfer-Eintrag `C_Opfer` fuer ein 4-Spieler-Spiel.【F:docs/requirements/constraints.md】
- Alle Charakter-IDs sind eindeutig.
- Alle Referenzen in `relationships.with`, `secrets.holders` und Alibi-Zeugen zeigen auf existierende Charaktere.
- `reveal_rule.earliest_round` liegt bei allen Geheimnissen im Bereich 1..4.
- `murder_context.is_murder` ist genau bei einer Rolle auf `true` gesetzt (`C_MOERDER`), alle anderen sind `false`.

## Hinweis zum Template-vs-Constraint-Konflikt
- Das Template `templates/characters.yaml` enthaelt kein explizites `alibi`-Feld.【F:templates/characters.yaml】
- Die Muss-Kriterien verlangen jedoch ausdruecklich Alibis inkl. `window` und Zeugen in `story/character.yaml`.【F:docs/requirements/constraints.md】
- Daher wurde `alibi` als notwendige, constraints-getriebene Erweiterung aufgenommen. Ohne dieses Feld waere Schritt 4 inhaltlich unvollstaendig.

## Logikprüfung
- Jede spielbare Rolle hat ein plausibles Motiv, ein belastbares Geheimnis und eine Gelegenheit, passend zur Storyline.【F:story/storyline】
- Alle Alibi-Zeitfenster sind formal gueltig (`start < end`).
- Alibi-`location_id` referenziert nur existierende Orte aus `story/locations.yaml` (`L_SALON`, `L_ARBEITSRAUM`, `L_TECHNIKRAUM`).【F:story/locations.yaml】
- C_Opfer enthaelt bewusst kein Alibi und kein Mordmotiv, entsprechend den Muss-Kriterien.【F:docs/requirements/constraints.md】

## Festgestellte harte Fehler
- Keine harten Logikfehler festgestellt.
- Keine Korrektur an `story/character.yaml` erforderlich.

## Hinweise für Schritt 5+
- Motiv-IDs aus `story/character.yaml` sollten in `story/motives.yaml` konsistent uebernommen werden.
- Alibi-Fenster muessen in `story/timeline.yaml` als Presence/Events ohne Widerspruch aufloesbar sein.【F:docs/requirements/constraints.md】

