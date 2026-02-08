# Muss-Kriterien fürs Funktionieren

**Zweck:** Prüfliste für Logik, Vollständigkeit und Spielbarkeit.
**Status:** Entwurf
**Letzte Änderung:** 2026-02-08

## Rahmenbedingungen
* Spiel ist für 4 SpielerInnen ausgelegt

## Logische Konsistenz
* Rollenbeschreibung, Hinweise und Auflösung dürfen sich nicht widersprechen; insbesondere muss der Tatablauf zu Alibis und Motiv passen.
* Hinweise müssen mit der Wahrheitspflicht kompatibel sein. Ausschließich Spieler des Mörders darf lügen.
* Alle Spieler:innen sind grundsätzlich verdächtig und jede Rolle muss ein plausibles Mordmotiv haben.
* jeder spieler kennt nur die Hinweise zum eigenen Charakter
* Jeder Charakter braucht ein Geheimnis, dessen Veröffentlichung den Charakter in Probleme und in Tatverdacht bringt


## Hinweisabdeckung
* Für jede Rolle existieren pro Hinweisrunde passende Hinweise oder Gerüchte gemäß Ablaufstruktur.
* Pflicht-Hinweise decken Tatablauf, Motiv und Gelegenheit ab; ohne sie ist die Auflösung nicht erreichbar.
* Hinweise sind rollenexklusiv: Nur die Rolle, die den Hinweis erhält, kennt ihn zu Beginn.
* Täter:in erhält Hinweise zu sich und belastenden vermeindlich Informationen über andere Charaktere und kann entscheiden diese zu teilen ,muss aber nicht.
* Es gibt klare Hinweise, die zum Täter/zur Täterin führen, aber auch Hinweise, die andere Personen plausibel erscheinen lassen, damit die Lösung nicht sofort eindeutig ist.
* In jeder Hinweisrunde gibt es mindestens einen neuen Hinweis, der auf eine Person deutet, aber nicht unbedingt auf den eigentlichen Mörder.
* Am Ende jedes Hinweises gibt es eine stichpunktartige Zusammenfassung dieses Hinweises





## Spielablauf (6 Akte)
### 1. Akt – Einführung
* Eine Person liest den Einführungstext vor. dieser beinhaltet das Setting der Geschichte sodass spieler sich in die Situation gut einfühlen können
* Danach stellen sich alle Charaktere kurz vor (Name, Rolle, Motivation). das tun sie anhand der Beschreibung seines Charakters die jeder spieler zuvor erhalten hat, um sich in den Charakter versetzen zu können.
* **Wichtig:** In dieser Phase noch keine Fragen stellen.  

### 2. Akt – Hinweisrunde 1
1. Hinweise 1 werden geheim ausgeteilt und gelesen.  es geht darin um Zeitlicher Ablauf (Wer war wann, wo und mit wem?) 
2. Falls vorhanden: Inspektor-Ergebnisse werden vorgelesen.  
3. Diskussion:  
   * Hinweise, die nicht die eigene Person belasten, sollen offen geteilt werden.  
   * Verdächtigungen und Rückfragen sind erlaubt.  
4. Die Runde endet, wenn alle Hinweise diskutiert wurden und keine Fragen mehr offen sind.  

### 3. Akt – Hinweisrunde 2
* Ablauf wie Hinweisrunde 1. es gejt dabei um vertiefende Information über das Opfer, die einen selbst oder/und andere Verdächtige belasten könnten. Suggestivfragen um Diskussion 

### 4. Akt – Hinweisrunde 3 (Gerüchterunde)
* Jede Rolle trägt ein Gerücht vor, das wahr oder falsch sein kann.  
* Ziel: herausfinden, welche Gerüchte stimmen.  

### 5. Akt – Hinweisrunde 4
* Ablauf wie Hinweisrunde 1. Konkrete Motive anderer Verdächtiger werden beschrieben und mit Fragen hinterlegt Auflösung

### 6. Akt – Auflösung
1. Jede Person notiert **verdeckt** ihren Verdacht (Name des Täters/der Täterin).  
2. Reihum: Zettel zeigen und begründen.  
3. Die „Auflösung“ wird vorgelesen – Ende des Spiels.  


## Materialvollständigkeit
* Zusätzlich zum Spielmaterial braucht die Erstellung einen Strukturplan in Akten (inkl. Prolog/Ablaufschritten)
* Für jede Rolle muss ein Charakterblatt mit Eigenschaften, Geheimnissen, Mordmotiv und Alibi vorliegen.
* Für die Tat muss ein Detailblatt mit Ursachenkette, genauem Tathergang, Folgen sowie Hinweisen und falschen Fährten vorliegen.
* Charaktere werden nach dem Beispiel in [`templates/characters.yaml`](templates/characters.yaml) erstellt: Eigenschaften, Beziehungen und Geheimnisse sind so zu gestalten, dass sie Konflikte und Dynamik erzeugen, die im Spielverlauf aufgedeckt werden können; 
   * Geheimnisse müssen eng mit Zielen und Beziehungen verknüpft sein, um die Spannung zu erhöhen.【F:templates/characters.yaml.】
   * Bei der Kreation eines Spiels muss unter `story/character.yaml` eine Datei mit den Charakteren des Spiels nach dem Vorbild von [`templates/characters.yaml`](templates/characters.yaml) erstellt werden.【F:templates/characters.yaml.
   * **Die Motive und Gründe für Geheimnisse müssen konkret, nachvollziehbar und logisch sein**. Es dürfen nie unkonkrete Personen oder Motive ohne Begründung vorkommen.
   * Wenn in `story/character.yaml` das Mordopfer genannt wird, soll es IMMER C_O_<Name des Opfers> heißen.
   * Alibis dürfen nicht so zu entkräften sein, z.B. NIEMALS Charakter 1 behauptet er sei mit Charakter 2 zusammengewesen und CHarakter 2 war nicht dort.
   * Es MUSS einen Eintrag für C_O_<Name des Opfers> geben. Motive und Alibis werden für diesen EIntrag nicht erstellt
   * Die Orte müssen Anhand von location_ID referenziert werden
   * Jede Charakter-ID MUSS eindeutig sein; alle Referenzen in `relationships.with`, `secrets.holders` und Alibi-Zeugen müssen auf existierende Charaktere zeigen.
   * Beziehungen dürfen keine Selbstreferenzen enthalten (`with` darf nicht die eigene ID sein) und sollen keine logischen Widersprüche zwischen Rollenbeschreibung und Spielverhalten erzeugen.
   * Jede Rolle MUSS mindestens ein belastbares Geheimnis mit konkretem Risiko (`stakes`) und auslösbarer Offenlegungsregel (`reveal_rule`) haben; `earliest_round` darf nur im Bereich 1..4 liegen.
   * Alibi-`window` muss formal gültig sein (`start < end`) und inhaltlich mit Timeline-Presence, Event-Reihenfolge und genannten Zeugen zusammenpassen.
   * Öffentliche Ziele, private Ziele und Motive dürfen sich nicht gegenseitig ausschließen; verdeckte Ziele müssen plausibel erklären, warum eine Rolle Informationen zurückhält.
   * Für ein Spiel mit X SpielerInnen muss es genau X spielbare Charaktere plus 1 Opfer-Eintrag geben; zusätzliche spielbare Rollen sind nur mit angepasstem Regelwerk zulässig.
* Motive werden nach dem Beispiel in [`templates/motives.yaml`](templates/motives.yaml) erstellt.【F:templates/motives.yaml】
   * Bei der Kreation eines Spiels muss unter `story/motives.yaml` eine Datei mit den Motiven des Spiels nach dem Vorbild von `templates/motives.yaml` erstellt werden.【F:templates/motives.yaml】
   * Für jede spielbare Rolle (alle außer `C_O_<Name des Opfers>`) MUSS mindestens ein Motiv vorhanden sein, damit alle Rollen plausibel verdächtig bleiben.
   * `character` MUSS auf eine existierende Charakter-ID aus `story/character.yaml` verweisen und darf nie `C_O_<Name des Opfers>` sein.
   * Jedes Motiv MUSS `murder: true|false` enthalten. Es darf insgesamt GENAU EIN Motiv mit `murder: true` geben; dieses MUSS zur Täterrolle in Auflösung, Timeline und Hinweisen passen.
   * Jedes Motiv MUSS belastende Hinweise (`clue_support.primary`) und ergänzende Hinweise (`clue_support.secondary`) enthalten. Verwendete `clue_id`-Referenzen müssen in den Hinweisdateien existieren und inhaltlich zum Motiv passen.
   * Jedes Motiv MUSS mindestens einen entlastenden Gegenhinweis in `counter_clues` enthalten, damit alternative Deutungen möglich sind und die Lösung nicht zu früh eindeutig wird.
   * `strength` MUSS im Bereich 1 bis 3 liegen und mit der Stärke der Hinweise logisch korrespondieren (starkes Motiv braucht stärkere oder mehrere Hinweise bzw. Gegenhinweise).
   * `narrative_notes.reveal_arc.earliest_round` und `peak_round` müssen zur 4-rundigen Hinweisstruktur passen (`1..4`) und `earliest_round <= peak_round` erfüllen.
   * Kein Motiv darf Timeline, Alibi oder Rollenwissen widersprechen; insbesondere dürfen Motive keine Handlungen behaupten, die laut Zeitablauf unmöglich sind.
* Hinweise werden nach dem Beispiel in [`templates/clues.yaml`](templates/clues.yaml) erstellt.【F:templates/clues.yaml】
   * Bei der Kreation eines Spiels muss unter `story/clues.yaml` eine Datei mit den Hinweisen des Spiels nach dem Vorbild von `templates/clues.yaml` erstellt werden.【F:templates/clues.yaml】
   * Jede `clue.id` MUSS eindeutig sein.
   * Pro Clue MUSS `timeline_links.related_beats` mindestens einen Beat/Event enthalten.
   * `points_to.suspects` MUSS nur existierende Charakter-IDs referenzieren; `points_to.motives` MUSS nur existierende Motiv-IDs aus `story/motives.yaml` referenzieren.
   * `reliability` MUSS im Bereich 1 bis 3 liegen.
   * `discoverability.earliest_round` MUSS im Bereich 1..4 liegen und zur geplanten Dramaturgie passen (`knowledge.initial_holders` und Freigabelogik dürfen dem nicht widersprechen).
   * `knowledge.initial_holders` MUSS nur existierende Charakter-IDs enthalten; bei `public_when_revealed: true` darf der Hinweis nach Offenlegung nicht als exklusives Rollenwissen behandelt werden.
   * Clues dürfen sich nicht gegenseitig oder mit Timeline/Alibis widersprechen; mehrdeutige Hinweise sind erlaubt, harte Faktenkonflikte nicht.
   * Es MUSS sowohl belastende als auch entlastende Hinweise geben, damit die Lösung nicht in Runde 1 eindeutig ist und trotzdem bis zur Auflösung herleitbar bleibt.
* Der zeitliche Ablauf rund um den Mord wird nach dem Beispiel in [`templates/timeline.yaml`](templates/timeline.yaml) erstellt. Folgedes MUSS eingehalten werden:
   * Charaktere KÖNNEN NICHT an zwei Orten gleichzeitig sein.
   * Es muss zu jeden Zeitpunkt klar sein, wer wo war.
   * Die Beat-IDs in `timeline.beats[].id` sind die kanonischen Referenzen für `story/clues.yaml -> timeline_links.related_beats`. Jede dort referenzierte Beat-ID MUSS in der Timeline exakt existieren.
   * Wenn `story/clues.yaml` vor `story/timeline.yaml` erstellt wurde, MUSS die Timeline alle bereits verwendeten Beat-IDs übernehmen oder die Clue-Referenzen im selben Arbeitsschritt konsistent aktualisieren. Verwaiste Referenzen sind unzulässig. Prüfe dass die Beat Referenzen aus `story/clues.yaml` und `story/timeline.yaml` NICHT zu Logikbrüchen führen -.
   * Für jedes Presence-Intervall gilt: `start < end`; Intervalle einer Person dürfen sich nicht überlappen.
   * Für das gesamte kritische Zeitfenster (mindestens von erstem relevanten Event bis `murder.discovered_at`) muss für jede spielbare Rolle ein Aufenthaltsstatus vorliegen (Ort oder explizit `unknown`).
   * `murder.time` muss innerhalb des abgedeckten Zeitfensters liegen und strikt vor `murder.discovered_at` liegen.
   * `murder.location` sowie alle Event- und Presence-Orte müssen in den bekannten Orts-IDs enthalten sein (z.B. `story/locations.yaml` / `timeline.meta.locations`).
   * Jede Alibi-Behauptung aus `story/character.yaml` MUSS sich in der Timeline als Event/Presence abbilden lassen (bestätigt, bestritten oder unsicher), ohne harte Widersprüche.
   * Falls `presence_refs` oder `witness` verwendet werden, müssen diese IDs existieren und zur angegebenen Zeit am angegebenen Ort plausibel anwesend sein.
   * Die Täterrolle muss über Timeline und Motive konsistent identifizierbar sein: Das `murder: true`-Motiv, Gelegenheit/Fenster und Tatzeit dürfen sich nicht widersprechen.
