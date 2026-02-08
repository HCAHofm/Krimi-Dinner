# Clues Nach Motiv

Generiert am: `2026-02-08T18:33:00+00:00`
Quellen: 【F:story/clues.yaml】, 【F:story/motives.yaml】, 【F:story/character.yaml】, 【F:story/locations.yaml】, 【F:story/timeline.yaml】

## `M_LEONIE_1`
Charakter: Dr. Leonie Winter (`C_DR_LEONIE_WINTER`)
Staerke: `2` | murder: `False`
Beschreibung: Leonie fuerchtete den Verlust ihrer Approbation wegen damaliger Falscheintraege.

### Referenzen In `motives.yaml`

| Bereich | Clue-ID | Existiert | Verlinkt auf Motiv | Notiz |
| --- | --- | --- | --- | --- |
| primary | `K_DOC_LEONIE_NOTIZBUCH` | ja | ja | Das Notizbuch enthaelt widerspruechliche Zeitangaben zur Erstversorgung und zum Notruf. |
| secondary | `K_WIT_LEONIE_KRISENGESPRAECH` | ja | ja | Eine Beobachtung beschreibt Leonies nervoeses Streitgespraech mit Elias kurz vor der Tat. |
| counter_clues | `K_PHY_LEONIE_MEDKIT` | ja | ja | Frisch geoeffnetes Material im Medkit macht ihre Versorgungsaussage plausibel. |

### Clues Mit `points_to.motives`

| Clue | Runde | Polarity | Typ | Rel | Suspects | Motive | Beats | Kurzfassung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `K_WIT_LEONIE_KRISENGESPRAECH` - Nervoeses Gespraech zwischen Leonie und Elias | 2 | belastend | testimony | 2 | Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `M_LEONIE_1` - Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `B_2030_GESTAENDNISFORDERUNG` (20:30, `L_ARBEITSZIMMER`) | Leonie hatte kurz vor der Tat sichtbaren Konflikt mit Elias.; Thema war ihre berufliche Verwundbarkeit.; Die Aussage erzeugt Motivdruck, aber keinen direkten Tatnachweis. |
| `K_PHY_LEONIE_MEDKIT` - Frisch geoeffnetes Medkit | 2 | entlastend | physical | 2 | Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `M_LEONIE_1` - Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `B_2052_LEONIE_MEDKITFENSTER` (20:52, `L_SCHLAFZIMMER_UNTEN`) | Spur stuetzt Leonies Alibi teilweise.; Sie schliesst eine kurze Abwesenheit nicht aus.; Die Entlastung bleibt daher begrenzt. |
| `K_DOC_LEONIE_NOTIZBUCH` - Notizbuch mit widerspruechlichen Zeiten | 3 | belastend | document | 3 | Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `M_LEONIE_1` - Dr. Leonie Winter (`C_DR_LEONIE_WINTER`) | `B_1945_OFFENER_STREIT` (19:45, `L_SPEISESAAL`) | Dokument bedroht Leonies berufliche Existenz direkt.; Es liefert ein klares Selbstschutzmotiv.; Als Schriftquelle ist der Hinweis sehr belastbar. |

## `M_GREGOR_1`
Charakter: Gregor Voss (`C_GREGOR_VOSS`)
Staerke: `3` | murder: `True`
Beschreibung: Elias besass ein zweites Dossier, das Gregors spaetere Aktenmanipulation belegte.

### Referenzen In `motives.yaml`

| Bereich | Clue-ID | Existiert | Verlinkt auf Motiv | Notiz |
| --- | --- | --- | --- | --- |
| primary | `K_DOC_GREGOR_ARCHIVZUGRIFF` | ja | ja | Archivprotokolle und Freigabevermerke zeigen Gregors indirekten Zugriff auf belastende Altakten. |
| secondary | `K_DIG_GREGOR_SATWARNUNG` | ja | ja | Ein digitaler Entwurf auf Elias' Geraet deutet an, dass Gregor die Nacht als letzte Frist erhielt. |
| counter_clues | `K_WIT_GREGOR_EINGANG` | ja | ja | Eine Aussage verortet Gregor kurz vor dem Schuss am Schluesselbrett und schafft scheinbare Distanz. |

### Clues Mit `points_to.motives`

| Clue | Runde | Polarity | Typ | Rel | Suspects | Motive | Beats | Kurzfassung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `K_WIT_GREGOR_EINGANG` - Gregor am Schluesselbrett | 1 | entlastend | testimony | 1 | Gregor Voss (`C_GREGOR_VOSS`) | `M_GREGOR_1` (moerderisch) - Gregor Voss (`C_GREGOR_VOSS`) | `B_2059_GREGOR_EINGANGSFENSTER` (20:59, `L_EINGANGSBEREICH`) | Gregor hat ein scheinbares Alibi am Eingangsbereich.; Der Eingangsbereich liegt direkt beim Schluesselbrett.; Die Beobachtung ist kurz und nicht durchgaengig. |
| `K_DIG_GREGOR_SATWARNUNG` - Entwurf auf Elias' Tablet zur Sofortweitergabe | 3 | belastend | digital | 2 | Gregor Voss (`C_GREGOR_VOSS`) | `M_GREGOR_1` (moerderisch) - Gregor Voss (`C_GREGOR_VOSS`) | `B_2059_GREGOR_EINGANGSFENSTER` (20:59, `L_EINGANGSBEREICH`), `B_2105_SCHUSS` (21:05, `L_ARBEITSZIMMER`) | Gregor war als Hauptziel der Enthuellung markiert.; Der Entwurf erklaert akuten Tatdruck in derselben Nacht.; Digitaler Hinweis ist interpretierbar, aber klar belastend. |
| `K_DOC_GREGOR_ARCHIVZUGRIFF` - Archivzugriffe ueber Mittelsmann | 4 | belastend | document | 3 | Gregor Voss (`C_GREGOR_VOSS`) | `M_GREGOR_1` (moerderisch) - Gregor Voss (`C_GREGOR_VOSS`) | `B_1945_OFFENER_STREIT` (19:45, `L_SPEISESAAL`) | Dokument verknuepft Gregor konkret mit spaeterer Aktenmanipulation.; Das schafft das staerkste Einzelmotiv fuer die Tat.; Die Spur passt direkt zur kanonischen Aufloesung. |
| `K_DOC_ZERRISSENE_GESTAENDNISSEITE` - Teilweise verbrannte Gestaendnisseite | 4 | belastend | document | 2 | Gregor Voss (`C_GREGOR_VOSS`) | `M_GREGOR_1` (moerderisch) - Gregor Voss (`C_GREGOR_VOSS`) | `B_2105_SCHUSS` (21:05, `L_ARBEITSZIMMER`), `B_2107_LEICHENFUND` (21:07, `L_ARBEITSZIMMER`) | Die Seite deutet auf gezielte Beweisvernichtung hin.; Der Inhalt verknuepft Gregor mit Aktenmanipulation.; Der Fund staerkt die Mordhypothese gegen Gregor deutlich. |
| `K_PHY_WAFFENSCHRANK_RUECKSTELLUNG` - Schluesselrueckstellung am Brett | 4 | belastend | physical | 2 | Gregor Voss (`C_GREGOR_VOSS`), Marco Steiner (`C_MARCO_STEINER`) | `M_GREGOR_1` (moerderisch) - Gregor Voss (`C_GREGOR_VOSS`) | `B_2105_SCHUSS` (21:05, `L_ARBEITSZIMMER`), `B_2107_LEICHENFUND` (21:07, `L_ARBEITSZIMMER`) | Jemand entnahm den Schluessel und brachte ihn zurueck.; Die Spur bindet den Tatablauf an den Eingangsbereich.; Sie belastet besonders Personen mit Zugang zum Schluesselbrett. |

## `M_HELENE_1`
Charakter: Helene Falk (`C_HELENE_FALK`)
Staerke: `2` | murder: `False`
Beschreibung: Ein oeffentlicher Skandal um Schweigegeld und Scheinrechnungen haette Helenes Firma ruiniert.

### Referenzen In `motives.yaml`

| Bereich | Clue-ID | Existiert | Verlinkt auf Motiv | Notiz |
| --- | --- | --- | --- | --- |
| primary | `K_DOC_HELENE_SCHEINRECHNUNG` | ja | ja | Mehrere Buchungen zeigen verdeckte Zahlungen nach dem Unfall und direkten Druck durch Elias. |
| secondary | `K_MSG_HELENE_ULTIMATUM` | ja | ja | Eine Nachricht belegt, dass Elias Helene mit sofortiger Veroeffentlichung bedrohte. |
| counter_clues | `K_WIT_HELENE_SALON` | ja | ja | Eine Zeugenaussage stuetzt, dass Helene zur Kernzeit zumindest zeitweise im Salon war. |

### Clues Mit `points_to.motives`

| Clue | Runde | Polarity | Typ | Rel | Suspects | Motive | Beats | Kurzfassung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `K_WIT_HELENE_SALON` - Helene blieb laut Gregor im Salon | 1 | entlastend | testimony | 1 | Helene Falk (`C_HELENE_FALK`) | `M_HELENE_1` - Helene Falk (`C_HELENE_FALK`) | `B_2050_HELENE_SALONFENSTER` (20:50, `L_SALON`) | Helene wird fuer einen Teil des Zeitfensters entlastet.; Die Entlastung kommt ausgerechnet von Gregor.; Die Aussage deckt nicht das komplette Tatfenster ab. |
| `K_DOC_HELENE_SCHEINRECHNUNG` - Scheinrechnungen nach dem Altfall | 2 | belastend | document | 3 | Helene Falk (`C_HELENE_FALK`) | `M_HELENE_1` - Helene Falk (`C_HELENE_FALK`) | `B_1945_OFFENER_STREIT` (19:45, `L_SPEISESAAL`), `B_2030_GESTAENDNISFORDERUNG` (20:30, `L_ARBEITSZIMMER`) | Die Unterlagen belegen finanzielles Risiko fuer Helene.; Damit wird ein starkes Motiv gegen Elias plausibel.; Der Beleg ist konkret und nachvollziehbar. |
| `K_MSG_HELENE_ULTIMATUM` - Ungelesene Ultimatum-Nachricht | 2 | belastend | digital | 2 | Helene Falk (`C_HELENE_FALK`) | `M_HELENE_1` - Helene Falk (`C_HELENE_FALK`) | `B_2050_HELENE_SALONFENSTER` (20:50, `L_SALON`) | Elias setzte Helene akut unter Zeitdruck.; Die Nachricht passt zu einem Eskalationsmotiv.; Da das Geraet privat ist, braucht es aktive Offenlegung. |

## `M_MARCO_1`
Charakter: Marco Steiner (`C_MARCO_STEINER`)
Staerke: `3` | murder: `False`
Beschreibung: Elias konnte Marcos Freigabe des beschaedigten Sicherungsseils direkt belegen.

### Referenzen In `motives.yaml`

| Bereich | Clue-ID | Existiert | Verlinkt auf Motiv | Notiz |
| --- | --- | --- | --- | --- |
| primary | `K_DOC_MARCO_SEILPROTOKOLL` | ja | ja | Das unterschriebene Wartungsprotokoll verknuepft Marco unmittelbar mit dem ignorierten Sicherheitsmangel. |
| secondary | `K_WIT_MARCO_GANG` | ja | ja | Eine Aussage platziert Marco kurz vor dem Schuss in Reichweite des oberen Gangs. |
| counter_clues | `K_PHY_MARCO_TECHNIKRESET` | ja | ja | Der manuelle Notstrom-Reset im Technikraum stuetzt teilweise Marcos Alibi. |

### Clues Mit `points_to.motives`

| Clue | Runde | Polarity | Typ | Rel | Suspects | Motive | Beats | Kurzfassung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `K_WIT_MARCO_GANG` - Marco im oberen Gang kurz vor dem Schuss | 1 | belastend | testimony | 2 | Marco Steiner (`C_MARCO_STEINER`) | `M_MARCO_1` - Marco Steiner (`C_MARCO_STEINER`) | `B_2103_BEWEGUNG_IM_GANG` (21:03, `L_OBERER_GANG`) | Marco wurde nahe Tatbereich gesehen.; Zeitlich liegt die Beobachtung unmittelbar vor dem Schuss.; Die Aussage stammt von Helene und ist daher interessengefaerbt. |
| `K_DOC_MARCO_SEILPROTOKOLL` - Wartungsprotokoll mit Marcos Freigabe | 2 | belastend | document | 3 | Marco Steiner (`C_MARCO_STEINER`) | `M_MARCO_1` - Marco Steiner (`C_MARCO_STEINER`) | `B_2030_GESTAENDNISFORDERUNG` (20:30, `L_ARBEITSZIMMER`) | Dokument belegt Marcos technische Mitverantwortung.; Der Beleg erklaert ein starkes Vertuschungsmotiv.; Es handelt sich um einen belastbaren Schriftbeweis. |
| `K_PHY_MARCO_TECHNIKRESET` - Notstrom-Reset im Technikraum | 2 | entlastend | physical | 3 | Marco Steiner (`C_MARCO_STEINER`) | `M_MARCO_1` - Marco Steiner (`C_MARCO_STEINER`) | `B_2048_MARCO_TECHNIKFENSTER` (20:48, `L_TECHNIKRAUM`), `B_2015_STROMFLACKERN` (20:15, `L_SALON`) | Technikspur stuetzt Marcos Erklaerung teilweise.; Der Eintrag beweist aber nicht seine Anwesenheit ueber das gesamte Fenster.; Das schafft gleichzeitige Entlastung und Restverdacht. |
