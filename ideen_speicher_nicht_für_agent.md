5) Kritischer Punkt zu deiner Regel “jeder Clue braucht related_beats”
Das macht es sehr prüfbar, aber du verlierst eine Klasse von Hinweisen:
längerfristige Fakten (z.B. „Schulden seit Monaten“)
Beziehungs-/Motiv-Hintergrund, der nicht an eine konkrete Szene gebunden ist
Wenn du trotzdem bei der Regel bleiben willst, gib solchen Clues einen eigenen Beat-Typ, z.B. B_BACKGROUND oder B_BEFORE_PARTY, damit es formal konsistent bleibt und trotzdem semantisch passt.


* Prüfe auf Korrektheit von Validate

* alibi erst später hinzufügen zu characters.yaml da es zu inkonsistenzen führen kann. Derzeit ist das noch nicht logisch. es kommen immer wieder dinge wie: Marco und Leonie nennen sich gegenseitig als Zeugen, sind aber im gleichen Überlappungsfenster an unterschiedlichen Orten:

Konsistenzcheck mithife des validate moduls sollte ein agent machen damit, er die Inhalte direkt anpassen kann.

  * `resolution-links.md` – welche Hinweise führen zu welcher Schlussfolgerung.





README schreiben: Die Aufgaben aus AGENTS.md müssen einzeln aktiv als Prompt ausgeführt werden. Wenn das Ergebnis nicht gut war, kann die neu erstellte Datei gelöscht werden und die Aufgabe noch einmal ausgeführt werden.
Erfahrungen die dabei gemacht werden und ggf hilreiche Regeln für den ki agent wären sollten in AGENTS.md oder constraints.md manuell geschrieben werden. So wird die dieses Repo Schritt für Schritt besser