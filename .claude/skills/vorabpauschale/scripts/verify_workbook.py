#!/usr/bin/env python3
"""Rechnet alle Formeln einer Vorabpauschale-Mappe nach und meldet Fehlerzellen.

openpyxl schreibt Formeln ohne Ergebniswerte. Ohne Nachrechnen bleibt daher
unbemerkt, wenn eine Formel #NAME?, #VALUE! oder #REF! liefert. Dieses Skript
wertet die Mappe mit der Bibliothek 'formulas' aus (reines Python, funktioniert
auch dort, wo LibreOffice keine xlsx-Dateien laden kann) und vergleicht die
Summen zusätzlich mit einer unabhängigen Nachrechnung derselben Eingabedaten.

Aufruf:
    python3 verify_workbook.py Mandant-Mueller-2025.xlsx
"""

import argparse
import datetime
import logging
import sys
import warnings

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)

try:
    import formulas
except ImportError:
    sys.exit("Bitte zuerst installieren:  pip install formulas")

from openpyxl import load_workbook

FIRST_ROW = 9


def zellwerte(pfad):
    """Wertet die Mappe aus und gibt {BLATT!ZELLE: Wert} zurück."""
    sol = formulas.ExcelModel().loads(pfad).finish().calculate()
    werte = {}
    for schluessel, zelle in sol.items():
        try:
            werte[schluessel.upper()] = zelle.value[0, 0]
        except Exception:
            continue
    return werte


def nachrechnen(pfad):
    """Rechnet Vorabpauschale und Steuer unabhängig aus den Eingabezellen nach."""
    wb = load_workbook(pfad)
    dp, sd = wb["Depot"], wb["Stammdaten"]

    jahr = dp["D4"].value
    basiszins = next((sd.cell(r, 3).value for r in range(6, 16)
                      if sd.cell(r, 2).value == jahr), None) or 0
    faktor = sd["C18"].value
    anlegerart = dp["D7"].value
    spalte = {"Privatvermögen": 3,
              "Betriebsvermögen (Einkommensteuer)": 4,
              "Betriebsvermögen (Körperschaftsteuer)": 5}[anlegerart]
    teilfrei = {sd.cell(r, 2).value: sd.cell(r, spalte).value for r in range(23, 28)}

    brutto = steuerpflichtig = 0.0
    zeile = FIRST_ROW
    while dp.cell(zeile, 3).value:
        art = dp.cell(zeile, 4).value
        anteile = dp.cell(zeile, 5).value or 0
        rp1 = dp.cell(zeile, 6).value or 0
        rp2 = dp.cell(zeile, 7).value or 0
        aus = dp.cell(zeile, 8).value or 0
        monat = dp.cell(zeile, 9).value
        basisertrag = max(0.0, rp1 * basiszins * faktor)
        mehrbetrag = max(0.0, (rp2 - rp1) + aus)
        monatsfaktor = 1.0 if monat in (None, "") else max(0.0, (13 - monat) / 12)
        gesamt = max(0.0, min(basisertrag, mehrbetrag) - aus) * monatsfaktor * anteile
        brutto += gesamt
        steuerpflichtig += gesamt * (1 - teilfrei[art])
        zeile += 1

    aw = wb["Auswertung"]
    frei = aw["C14"].value or 0
    kirchensteuer = sd["C33"].value or 0
    kapst_satz = sd["C31"].value
    solz_satz = sd["C32"].value
    bmg = max(0.0, steuerpflichtig - min(frei, max(0.0, steuerpflichtig)))
    kapst = bmg * kapst_satz / (1 + kapst_satz * kirchensteuer)
    return {"brutto": brutto, "steuerpflichtig": steuerpflichtig, "bmg": bmg,
            "kapst": kapst, "gesamt": kapst * (1 + solz_satz + kirchensteuer)}


def summenzeile(pfad):
    """Findet die Zeile mit den Depotsummen (steht unterhalb des Eingabebereichs)."""
    dp = load_workbook(pfad)["Depot"]
    for r in range(FIRST_ROW, dp.max_row + 1):
        if dp.cell(r, 3).value == "Summe Depot":
            return r
    raise SystemExit("Summenzeile im Blatt 'Depot' nicht gefunden.")


def main():
    ap = argparse.ArgumentParser(description="Vorabpauschale-Mappe nachrechnen")
    ap.add_argument("datei")
    args = ap.parse_args()

    werte = zellwerte(args.datei)
    praefix = next(k for k in werte if "]DEPOT'!" in k).split("]")[0] + "]"
    hole = lambda blatt, zelle: werte.get(f"{praefix}{blatt}'!{zelle}")

    fehler = sorted((k, str(v)) for k, v in werte.items()
                    if str(v).startswith("#") and str(v) != "#EMPTY")
    print(f"Zellen ausgewertet : {len(werte)}")
    print(f"Fehlerzellen       : {len(fehler)}")
    for schluessel, wert in fehler[:25]:
        print("   ", schluessel, "->", wert)

    erwartet = nachrechnen(args.datei)
    abgleich = [
        ("Vorabpauschale brutto", hole("DEPOT", f"O{summenzeile(args.datei)}"), erwartet["brutto"]),
        ("Bemessungsgrundlage", hole("AUSWERTUNG", "C16"), erwartet["bmg"]),
        ("Kapitalertragsteuer", hole("AUSWERTUNG", "C20"), erwartet["kapst"]),
        ("Gesamte Steuerbelastung", hole("AUSWERTUNG", "C23"), erwartet["gesamt"]),
    ]

    print("\nAbgleich mit unabhängiger Nachrechnung:")
    abweichungen = 0
    for bezeichnung, ist, soll in abgleich:
        try:
            passt = abs(float(ist) - float(soll)) < 0.005
        except (TypeError, ValueError):
            passt = False
        abweichungen += not passt
        print(f"  {'OK ' if passt else 'ABW'} {bezeichnung:24} Mappe={ist}  Nachrechnung={soll}")

    zufluss = hole("AUSWERTUNG", "C8")
    try:
        datum = datetime.date(1899, 12, 30) + datetime.timedelta(days=float(zufluss))
        wochenende = datum.weekday() >= 5
        neujahr = (datum.month, datum.day) == (1, 1)
        print(f"\nZuflusstag: {datum:%d.%m.%Y} ({datum:%a})"
              + ("  ACHTUNG: kein Werktag" if wochenende or neujahr else ""))
        abweichungen += wochenende or neujahr
    except (TypeError, ValueError):
        print(f"\nZuflusstag: nicht auswertbar ({zufluss!r})")
        abweichungen += 1

    gesamt = len(fehler) + abweichungen
    print("\nERGEBNIS:", "Mappe ist in Ordnung" if gesamt == 0
          else f"{gesamt} Beanstandung(en) – bitte beheben")
    return 1 if gesamt else 0


if __name__ == "__main__":
    sys.exit(main())
