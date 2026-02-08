# Plan: Anforderungen definieren & sammeln, damit das Krimi-Dinner spielbar ist

## Ziel
Wir brauchen eine verlässliche Definition dessen, was eingehalten werden muss, damit das Krimi‑Dinner im Spiel funktioniert. Dafür sammeln wir die nötigen Informationen strukturiert, legen sie nachvollziehbar ab und leiten daraus eindeutige Spielanforderungen ab.

## 1) Welche Informationen brauchen wir?
Diese Liste orientiert sich an den bereits dokumentierten Regeln, dem Spielablauf und den vorhandenen Dokumenttypen (Einladung, Rollen, Hinweise, Auflösung).

### A. Spielmechanik & Ablauf
* Phasen/Acts mit klaren Zielen und Timing (Einführung, Hinweisrunden, Gerüchterunde, Auflösung).
* Regeln zu Wahrheitspflicht, Lügenregel, Improvisation und Umgang mit Wissenslücken.
* Mindestanzahl an Hinweisen je Runde und pro Rolle (abgeleitet aus Hinweisrunden‑Struktur).

### B. Narrativ & Logik
* Tatablauf, Motiv, Gelegenheit (timeline + alibis).【F:rules_for_krimidinner.md†L6-L12】
* Konsistenz zwischen Rollenbeschreibung, Hinweisen und Auflösung (keine Widersprüche).

### C. Rollen & Balance
* Anzahl Rollen, Verhältnis Täter/Ermittler, Informationsverteilung pro Rolle (wer weiß was, wann).
* Konfliktpotenzial und Verdachtsmomente pro Rolle.

### D. Material & Dokumente
* Verpflichtende Dokumente: Einführungstext, Rollenbeschreibungen, Hinweishefte, Auflösungstext, Einladung/Regeln/Ortsbeschreibung/Charakterübersicht.【F:rules_for_krimidinner.md†L16-L24】
* Struktur-Verbesserungen aus Erfahrungskritik (Hinweisübersicht, Kurzfassung je Runde, Entscheidungsmerkmal zur Überführung).【F:rules_for_krimidinner.md†L26-L33】

## 2) Wie erhalten wir diese Informationen?

### Schritt 1: Ist‑Analyse vorhandener Regeln & Beispiele
* Extrahiere Regeln, Ablauf, Dokumentarten und bekannte Schwächen aus den vorhandenen Regelwerken und Spielnotizen.
* Ergebnis: konsolidierte Liste „Muss‑Regeln“ + „Nice‑to‑have“.

### Schritt 2: Story‑Design Workshop (intern)
* Erstelle einen Tatablauf (Zeitlinie), Motive, Tatgelegenheit, Opferprofil.
* Leite daraus Rollenprofile und konfliktträchtige Beziehungen ab.

### Schritt 3: Informations‑Mapping
* Baue eine Matrix „Rolle × Runde“ für Hinweise, Gerüchte, Verdachtsmomente.
* Kennzeichne Pflicht‑Hinweise (für Auflösung nötig) vs. optionale Hinweise (Atmosphäre).

### Schritt 4: Konsistenz‑Checks
* Prüfe Widersprüche zwischen Rollen, Hinweisen und Auflösung.
* Validierung anhand der „Wahrheitspflicht/Lügenregel“ (wer darf was behaupten).

### Schritt 5: Playtest‑Feedback
* Kurzer Probelauf mit 2–3 Personen zur Prüfung von:
  * Hinweislänge/Überfrachtung (Problem laut Erfahrungskritik).【F:rules_for_krimidinner.md†L26-L33】
  * Verständlichkeit der Auflösung.
* Optional: Ein Testlauf kann zusätzlich durch KI‑Agenten simuliert werden, um Logikbrüche oder Informationslücken früh zu erkennen.

## 3) Wie legen wir die Informationen ab?

### A. Single‑Source‑of‑Truth (Ordnerstruktur)
* `docs/requirements/`
  * `gameplay_guidelines.md` – verbindliche Spielregeln & Ablauf (konsolidiert).
  * `constraints.md` – Muss‑Kriterien fürs Funktionieren (Widerspruchsfreiheit, Hinweisabdeckung, etc.).
  * `experience_fixes.md` – verpflichtende Verbesserungen (Hinweisübersicht, Kurzfassungen, entscheidendes Merkmal).【F:rules_for_krimidinner.md†L26-L33】
* `docs/story/`
  * `timeline.md` – Tatablauf & Alibis.
  * `characters.md` – Rollenprofile, Beziehungen, Motive.
* `docs/hints/`
  * `hint-matrix.md` – Rolle × Runde, Pflicht/Optional‑Hinweise.
  * `resolution-links.md` – welche Hinweise führen zu welcher Schlussfolgerung.

### B. Format‑Konvention
* Jede Datei enthält:
  * **Zweck**, **Status** (Entwurf/Final), **Letzte Änderung**.
  * Bei Hinweisen: Referenz zur Rolle und Runde.

## 4) Output, der am Ende vorliegen muss
* Konsolidiertes Regelwerk + Ablauf, damit alle dieselben Spielregeln nutzen.
* Vollständige Dokumentliste inklusive Verbesserungen aus der Erfahrungskritik.【F:rules_for_krimidinner.md†L16-L33】
* Hinweis‑Matrix und Tat‑Timeline zur Absicherung der Logik.

---

**Nächster Schritt (Vorschlag):**
1) `docs/requirements/gameplay_guidelines.md` aus den vorhandenen Regeln konsolidieren.  
2) Tat‑Timeline entwerfen und Rollen daraus ableiten.  
3) Hinweis‑Matrix aufbauen und Pflicht‑Hinweise definieren.
