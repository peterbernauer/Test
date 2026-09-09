---
name: vorabpauschale
description: Erstellt ein formelbasiertes Excel-Werkzeug zur Ermittlung der Vorabpauschale nach § 18 InvStG für ein bestehendes Depot - je Fondsposition Basisertrag, Begrenzung auf den Mehrbetrag, Abzug der Ausschüttungen, Monatsanteil im Erwerbsjahr und Teilfreistellung nach § 20 InvStG, dazu Kapitalertragsteuer, Solidaritätszuschlag und Kirchensteuer. Nutze diesen Skill, wenn Peter nach der "Vorabpauschale" fragt, nach der laufenden Besteuerung von Investmentfonds oder ETF im Depot, nach "Basisertrag", "Basiszins", "Teilfreistellung", nach der Versteuerung thesaurierender Fonds, nach dem Steuereinzug der Bank zum Jahresanfang oder danach, wie viel Liquidität ein Mandant dafür vorhalten muss - auch bei nur einzelnen Eckdaten (Fondsbestand, Rücknahmepreise, Ausschüttungen) oder beim Weiterentwickeln einer damit erstellten Mappe.
---

# Vorabpauschale für ein bestehendes Depot

Peter ist Steuerberater. Die Mappe, die dieser Skill erzeugt, geht an Mandanten oder
dient der eigenen Prüfung — sie muss deshalb nachvollziehbar rechnen und darf keine
stillen Annahmen enthalten. Zwei Dinge folgen daraus und ziehen sich durch alles
Weitere: **jede Zahl bleibt eine lebende Formel** (nie ein in Python ausgerechnetes
Ergebnis, sonst rechnet die Mappe beim Ändern eines Rücknahmepreises nicht nach), und
**fehlende Angaben werden erfragt, nicht geschätzt**. Ein geratener Rücknahmepreis
sieht in Excel genauso aus wie ein echter.

## Ablauf

**1. Eckdaten klären.** Nötig sind Steuerjahr, Anlegerart (Privat- oder
Betriebsvermögen) und je Fondsposition die Angaben aus dem nächsten Abschnitt. Frage
nach dem, was fehlt. Wenn Peter nur grob beschreibt („ein Depot mit drei ETF"), bau
die Mappe mit den Beispielzeilen und lass ihn die echten Zahlen eintragen — das ist
schneller als ein langes Interview.

**2. Positionen erfassen.** Liegen konkrete Zahlen vor, schreib sie in eine
JSON-Datei (Schema unten) und übergib sie dem Generator. Ohne Positionsdatei enthält
die Mappe vier Beispielzeilen zum Überschreiben.

**3. Mappe erzeugen.**

```bash
python3 scripts/build_workbook.py --out "Mandant-Mueller-2025.xlsx" \
    --jahr 2025 --mandant "Eheleute Müller" --positionen depot.json
```

`--zeilen N` steuert die Zahl der Eingabezeilen (Standard 25). Ohne `--positionen`
entstehen Beispieldaten.

**4. Nachrechnen — nicht überspringen.**

```bash
python3 scripts/verify_workbook.py "Mandant-Mueller-2025.xlsx"
```

openpyxl schreibt Formeln ohne Ergebniswerte. Eine Formel, die `#NAME?` oder
`#VALUE!` liefert, fällt sonst erst dem Mandanten auf. Das Skript wertet jede Zelle
aus, vergleicht die Summen mit einer unabhängigen Nachrechnung und prüft, ob der
Zuflusstag tatsächlich ein Werktag ist. Liefere nichts aus, solange es Beanstandungen
meldet. Es braucht `pip install formulas`; LibreOffice ist als Alternative unzuverlässig
und kann in manchen Umgebungen gar keine xlsx-Dateien laden.

**5. Übergeben.** Nenne Peter die Gesamtbelastung und den Zuflusstag, und weise auf
die beiden Punkte hin, die er selbst verantworten muss: die Basiszinssätze in den
Stammdaten sind gegen das BMF-Schreiben abzugleichen, und ist das Steuerjahr dort noch
nicht hinterlegt, warnt die Mappe aktiv und rechnet mit null.

## Angaben je Position

| Feld | Bedeutung |
|---|---|
| `isin` | ISIN oder WKN |
| `bezeichnung` | Fondsname |
| `fondsart` | genau einer von: `Aktienfonds`, `Mischfonds`, `Immobilienfonds`, `Auslands-Immobilienfonds`, `Sonstiger Fonds` |
| `anteile` | Bestand am 31.12., Bruchteile erlaubt |
| `rp_anfang` | Rücknahmepreis am ersten Bewertungstag des Kalenderjahres, je Anteil |
| `rp_ende` | Rücknahmepreis am letzten Bewertungstag, je Anteil |
| `ausschuettung` | Ausschüttungen des Kalenderjahres, je Anteil |
| `erwerbsmonat` | 1–12, wenn im Steuerjahr erworben; sonst `null` |

```json
{"mandant": "Eheleute Müller",
 "positionen": [
   {"isin": "IE00B4L5Y983", "bezeichnung": "iShares Core MSCI World",
    "fondsart": "Aktienfonds", "anteile": 250, "rp_anfang": 88.50,
    "rp_ende": 101.20, "ausschuettung": 0.0, "erwerbsmonat": null}
 ]}
```

Die Fondsart entscheidet über die Teilfreistellung und ist damit der teuerste
Fehler in der Kette. Sie ergibt sich aus der Kapitalbeteiligungsquote in den
Anlagebedingungen, nicht aus dem Fondsnamen — ein „Multi-Asset"-Fonds kann
Mischfonds oder sonstiger Fonds sein. Im Zweifel nachfragen statt raten.

## Rechenweg

Je Anteil, in dieser Reihenfolge:

1. **Basisertrag** = Rücknahmepreis am Jahresanfang × Basiszins × 70 %
2. **Begrenzung** auf den Mehrbetrag = (Rücknahmepreis Jahresende − Jahresanfang) + Ausschüttungen
3. **Vorabpauschale** = begrenzter Basisertrag − Ausschüttungen, mindestens null
4. **Monatsanteil** im Erwerbsjahr: ein Zwölftel weniger je vollem Monat vor dem Erwerbsmonat
5. × Anteilsbestand, dann **Teilfreistellung** nach § 20 InvStG

Details, Fundstellen und die Basiszinsreihe stehen in `references/rechtsgrundlagen.md`.
Lies die Datei, wenn Peter nach der Herleitung fragt, eine Sonderkonstellation
auftaucht (Betriebsvermögen, unterjähriger Verkauf, Anteilsscheinklassen) oder du
einen Basiszins nachtragen musst.

## Stolperstellen

**Der Mehrbetrag ist die eigentliche Bremse.** In einem Jahr mit Kursverlust ist die
Vorabpauschale null, auch wenn der Basiszins hoch war. Ausschüttungen zehren sie
zusätzlich auf und können sie ebenfalls auf null drücken. Wenn eine Position
überraschend null ergibt, ist das meist kein Fehler — prüf Schritt 2 und 3, bevor du
etwas „korrigierst".

**Negativer Basiszins.** 2021 (−0,45 %) und 2022 (−0,05 %) fällt gar keine
Vorabpauschale an. Die Mappe zeigt dann einen Hinweis und rechnet mit null.

**Unterjährig verkaufte Positionen gehören nicht in die Tabelle.** Die
Vorabpauschale gilt erst am ersten Werktag des Folgejahres als zugeflossen; wer bis
dahin verkauft hat, versteuert stattdessen den Veräußerungsgewinn.

**Die Bank rechnet immer mit den Privatanlegersätzen.** Die höheren
Teilfreistellungssätze im Betriebsvermögen wirken erst in der Veranlagung. Wenn Peter
die Anlegerart auf Betriebsvermögen stellt, zeigt die Mappe die
Veranlagungssicht — sag dazu, dass der Steuerabzug der Bank abweicht.

**Zuflusstag ist nie der 1. Januar.** Der ist stets Feiertag. Die Mappe rechnet den
ersten Werktag danach aus; regionale Feiertage wie der 6. Januar bleiben unberücksichtigt.

**Versteuerte Vorabpauschalen mindern später den Veräußerungsgewinn** (§ 19 Abs. 1
Satz 4 InvStG). Die Mappe schreibt das nicht fort — weise darauf hin, wenn ein
Verkauf im Raum steht.

## Weiterentwickeln einer bestehenden Mappe

Kommt Peter mit einer schon erzeugten Datei zurück, ändere sie mit openpyxl direkt und
lass die Formeln stehen; die Eingabezellen sind gelb hinterlegt mit blauer Schrift, alles
Graue rechnet. Danach wieder `verify_workbook.py` laufen lassen. Nur wenn sich der
Aufbau selbst ändern soll (andere Spalten, mehr Blätter), lohnt es, den Generator
anzupassen und neu zu bauen — dann gehen allerdings von Hand eingetragene Werte verloren,
also vorher fragen.
