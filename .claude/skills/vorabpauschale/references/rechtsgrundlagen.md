# Rechtsgrundlagen der Vorabpauschale

Inhalt: [Rechenweg](#rechenweg-nach--18-invstg) · [Basiszins](#basiszins) ·
[Teilfreistellung](#teilfreistellung-nach--20-invstg) · [Steuerabzug](#steuerabzug) ·
[Sonderfälle](#sonderfälle) · [Aufbau der Mappe](#aufbau-der-erzeugten-mappe)

Rechtsstand: InvStG in der ab 2018 geltenden Fassung. Alle Angaben sind vor
Verwendung in der Beratung am Gesetzestext und am aktuellen BMF-Schreiben zu
verifizieren.

> **Zu den Absatzangaben.** Die Zuordnung der Regelungen zu den einzelnen Absätzen
> des § 18 InvStG stammt aus Modellwissen und wurde nicht gegen den Gesetzestext
> abgeglichen — in der Umgebung, in der dieser Skill entstand, war der Netzzugriff
> gesperrt. Die Zuordnung unten (Abs. 1 Definition, Abs. 2 Basisertrag und
> Begrenzung, Abs. 3 Basiszins, Abs. 4 Zufluss, Abs. 5 Zwölftelung) ist die
> gebräuchliche, aber ein Testlauf ordnete die Zuflussfiktion abweichend Abs. 3
> Satz 2 zu. Prüfe die Absatznummer, bevor sie in einem Mandantenschreiben oder
> Schriftsatz zitiert wird. Der Rechenweg selbst ist davon nicht betroffen.

## Rechenweg nach § 18 InvStG

Die Vorabpauschale besteuert bei thesaurierenden und schwach ausschüttenden Fonds
einen typisierten Mindestertrag, damit die Besteuerung nicht bis zum Verkauf
aufgeschoben wird. Sie fällt je Investmentanteil an:

| Schritt | Formel | Fundstelle |
|---|---|---|
| Basisertrag | Rücknahmepreis am ersten Bewertungstag des Kalenderjahres × Basiszins × 70 % | § 18 Abs. 2 Satz 1 |
| Begrenzung | höchstens der Mehrbetrag: (Rücknahmepreis letzter Bewertungstag − erster Bewertungstag) + Ausschüttungen | § 18 Abs. 2 Satz 2 |
| Vorabpauschale | begrenzter Basisertrag − Ausschüttungen des Kalenderjahres, mindestens null | § 18 Abs. 1 |
| Erwerbsjahr | Minderung um ein Zwölftel je vollem Monat vor dem Erwerbsmonat | § 18 Abs. 5 |
| Zufluss | erster Werktag des folgenden Kalenderjahres | § 18 Abs. 4 |

Der Faktor 70 % ist gesetzlich festgeschrieben. Die Begrenzung auf den Mehrbetrag
sorgt dafür, dass in Verlustjahren keine Vorabpauschale entsteht — sie ist der Grund,
warum ein hoher Basiszins allein noch keine Steuer auslöst.

Maßgeblich ist der Rücknahmepreis. Wird keiner festgesetzt, tritt der Börsen- oder
Marktpreis an seine Stelle (§ 6 InvStG); bei börsengehandelten ETF ist das in der
Regel der Schlusskurs beziehungsweise der veröffentlichte NAV.

## Basiszins

Der Basiszins wird aus der langfristig erzielbaren Rendite öffentlicher Anleihen
abgeleitet und bezieht sich auf den ersten Börsentag des Jahres; das BMF
veröffentlicht ihn im Bundessteuerblatt Teil I (§ 18 Abs. 3 InvStG).

| Jahr | Basiszins | davon 70 % | Anmerkung |
|---|---|---|---|
| 2018 | 0,87 % | 0,609 % | |
| 2019 | 0,52 % | 0,364 % | |
| 2020 | 0,07 % | 0,049 % | |
| 2021 | −0,45 % | — | negativ, keine Vorabpauschale |
| 2022 | −0,05 % | — | negativ, keine Vorabpauschale |
| 2023 | 2,55 % | 1,785 % | |
| 2024 | 2,29 % | 1,603 % | |
| 2025 | 2,53 % | 1,771 % | |
| ab 2026 | offen | | in den Stammdaten nachzutragen |

Diese Reihe ist nicht aus einer Primärquelle abgerufen, sondern hinterlegtes Wissen.
Gleich beim ersten Einsatz gegen die BMF-Schreiben abgleichen und die Mappe
korrigieren, falls ein Wert abweicht. Ein falscher Basiszins verfälscht jede Position
proportional.

Zum Nachtragen: im Blatt **Stammdaten** in der Basiszinstabelle (Spalte C) den Wert
als Dezimalzahl eintragen, also `0,0253` für 2,53 %. Fehlt der Wert, warnt das Blatt
Depot in Zelle F4 und rechnet mit null.

## Teilfreistellung nach § 20 InvStG

Die Teilfreistellung gleicht die Vorbelastung auf Fondsebene aus. Sie greift auf die
Vorabpauschale genauso wie auf Ausschüttungen und Veräußerungsgewinne.

| Fondsart | Voraussetzung | Privatvermögen | BV / ESt | BV / KSt |
|---|---|---|---|---|
| Aktienfonds | fortlaufend mind. 51 % Kapitalbeteiligungen | 30 % | 60 % | 80 % |
| Mischfonds | fortlaufend mind. 25 % Kapitalbeteiligungen | 15 % | 30 % | 40 % |
| Immobilienfonds | fortlaufend mind. 51 % Immobilien und Immobiliengesellschaften | 60 % | 60 % | 60 % |
| Auslands-Immobilienfonds | fortlaufend mind. 51 % ausländische Immobilien | 80 % | 80 % | 80 % |
| Sonstiger Fonds | — | 0 % | 0 % | 0 % |

Die Quote muss sich aus den Anlagebedingungen ergeben (§ 2 Abs. 6 InvStG) — der Name
des Fonds sagt darüber nichts aus. Beim Kapitalertragsteuerabzug wendet die
depotführende Stelle immer die Privatanlegersätze an; die höheren Sätze im
Betriebsvermögen wirken erst in der Veranlagung.

## Steuerabzug

Auf den nach Teilfreistellung verbleibenden Ertrag, gemindert um einen noch freien
Sparer-Pauschbetrag (1.000 € Einzel-, 2.000 € Zusammenveranlagung seit 2023):

- **Kapitalertragsteuer** 25 % (§ 43a Abs. 1 EStG)
- **Solidaritätszuschlag** 5,5 % auf die Kapitalertragsteuer — für Kapitalerträge
  unverändert zu erheben
- **Kirchensteuer** 8 % (Bayern, Baden-Württemberg) oder 9 %

Bei Kirchensteuerpflicht mindert der Sonderausgabenabzug bereits die
Bemessungsgrundlage des Steuerabzugs (§ 32d Abs. 1 Satz 3 EStG). Die Mappe rechnet:

```
Kapitalertragsteuer = Bemessungsgrundlage × 25 % / (1 + 25 % × Kirchensteuersatz)
```

Das ergibt 24,45 % bei 9 % Kirchensteuer und 24,51 % bei 8 %; ohne Kirchensteuer
bleibt es bei 25 %. Die Gesamtbelastung beträgt 26,375 % ohne und rund 27,82 % bis
27,99 % mit Kirchensteuer.

Die Bank zieht den Betrag vom Verrechnungskonto ein (§ 44 Abs. 1 Satz 11 EStG).
Reicht die Deckung nicht, meldet sie den nicht abgeführten Betrag dem Finanzamt und
der Mandant versteuert ihn in der Veranlagung. Das ist der praktische Grund, die
Gesamtbelastung im Januar als Liquiditätsbedarf auszuweisen.

## Sonderfälle

**Unterjähriger Verkauf.** Wer die Anteile vor dem Zuflusszeitpunkt veräußert hat,
schuldet für dieses Jahr keine Vorabpauschale; besteuert wird der
Veräußerungsgewinn. Solche Positionen gehören nicht in die Tabelle.

**Unterjähriger Erwerb.** Der Monatsanteil nach § 18 Abs. 5 InvStG kürzt die
Vorabpauschale, nicht den Basisertrag — die Kürzung wirkt also erst nach Abzug der
Ausschüttungen. Erwerb im April bedeutet drei volle Monate davor, Faktor 9/12.
Anzusetzen sind nur die nach dem Erwerb vereinnahmten Ausschüttungen.

**Anrechnung beim Verkauf.** Versteuerte Vorabpauschalen mindern den steuerpflichtigen
Veräußerungsgewinn (§ 19 Abs. 1 Satz 4 InvStG). Sie sind je Position fortzuschreiben;
die Mappe leistet das nicht.

**Mehrere Tranchen derselben ISIN.** Unterschiedliche Erwerbsmonate erfordern
getrennte Zeilen, weil der Monatsfaktor je Tranche abweicht. Bestände aus Vorjahren
und im Steuerjahr erworbene Anteile also nicht zusammenfassen.

**Betriebsvermögen.** Die Anlegerart im Blatt Depot stellt die Teilfreistellung um
und zeigt damit die Veranlagungssicht. Der Steuerabzug der Bank bleibt davon
unberührt — beim Ausweis dazusagen.

## Aufbau der erzeugten Mappe

| Blatt | Inhalt |
|---|---|
| Anleitung | Rechenweg, Bedienung, Praxishinweise, Haftungsausschluss |
| Stammdaten | Basiszinsreihe, Teilfreistellungssätze, Steuersätze, Sparer-Pauschbetrag, Auswahllisten |
| Depot | je Position Spalten B–I zur Eingabe, J–R als Berechnung, Summenzeile darunter |
| Auswertung | Bemessungsgrundlage, Steuerabzug, Aufteilung nach Fondsarten, Hinweise |

Farbkonvention: gelbe Füllung mit blauer Schrift = Eingabe, grau = Formel, grüne
Schrift = Verweis auf ein anderes Blatt. Die Berechnungsspalten im Blatt Depot sind
zeilenweise identisch aufgebaut; zusätzliche Positionen entstehen durch Kopieren einer
vorhandenen Zeile innerhalb des Tabellenbereichs, damit die Formeln mitgehen.
