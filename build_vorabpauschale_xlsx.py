#!/usr/bin/env python3
"""Erzeugt das Excel-Werkzeug 'Vorabpauschale-Rechner.xlsx' (§ 18 InvStG)."""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "Vorabpauschale-Rechner.xlsx"

FIRST_ROW, LAST_ROW = 9, 33          # Datenzeilen im Blatt "Depot"
SUM_ROW = 35

# ---------------------------------------------------------------- Formatierung
ARIAL = "Arial"
F_TITLE = Font(name=ARIAL, size=14, bold=True, color="1F3864")
F_SEC = Font(name=ARIAL, size=11, bold=True, color="1F3864")
F_HDR = Font(name=ARIAL, size=9, bold=True, color="FFFFFF")
F_BASE = Font(name=ARIAL, size=10)
F_BOLD = Font(name=ARIAL, size=10, bold=True)
F_IN = Font(name=ARIAL, size=10, color="0000FF")          # Eingabe = blau
F_LINK = Font(name=ARIAL, size=10, color="008000")        # Blattverweis = gruen
F_NOTE = Font(name=ARIAL, size=9, italic=True, color="595959")
F_WARN = Font(name=ARIAL, size=10, bold=True, color="C00000")

FILL_HDR = PatternFill("solid", fgColor="1F3864")
FILL_IN = PatternFill("solid", fgColor="FFFF00")          # Eingabezelle = gelb
FILL_CALC = PatternFill("solid", fgColor="F2F2F2")
FILL_SUM = PatternFill("solid", fgColor="D9E2F3")
FILL_SEC = PatternFill("solid", fgColor="DDEBF7")

THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

EUR = '#,##0.00" €"'
EUR4 = '#,##0.0000" €"'
PCT = '0.00%'
PCT0 = '0.0%'
STK = '#,##0.000'

wb = Workbook()

# ================================================================= 1 ANLEITUNG
ws = wb.active
ws.title = "Anleitung"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 46
ws.column_dimensions["C"].width = 96

def a(row, b_val, c_val="", bfont=F_BASE, cfont=F_BASE):
    ws.cell(row=row, column=2, value=b_val).font = bfont
    ws.cell(row=row, column=2).alignment = Alignment(vertical="top", wrap_text=True)
    if c_val != "":
        ws.cell(row=row, column=3, value=c_val).font = cfont
        ws.cell(row=row, column=3).alignment = Alignment(vertical="top", wrap_text=True)

def sec(row, text):
    for col in (2, 3):
        ws.cell(row=row, column=col).fill = FILL_SEC
    ws.cell(row=row, column=2, value=text).font = F_SEC

ws["B2"] = "Vorabpauschale-Rechner für Investmentfonds und ETF"
ws["B2"].font = F_TITLE
a(3, "Ermittlung der Vorabpauschale nach § 18 InvStG für ein bestehendes Depot", "", F_NOTE)

sec(5, "1. Aufbau der Arbeitsmappe")
a(6, "Stammdaten", "Basiszins je Kalenderjahr, Teilfreistellungssätze nach § 20 InvStG, Steuersätze und Sparer-Pauschbetrag. Hier wird der Basiszins für neue Jahre nachgetragen.")
a(7, "Depot", "Haupteingabe: eine Zeile je Fondsposition. Links die Eingabespalten (gelb), rechts die automatische Berechnung (grau).")
a(8, "Auswertung", "Summen, Sparer-Pauschbetrag, Kapitalertragsteuer, Solidaritätszuschlag, Kirchensteuer sowie eine Aufteilung nach Fondsarten.")

sec(10, "2. Bedienung in vier Schritten")
a(11, "Schritt 1", "Im Blatt 'Stammdaten' prüfen, ob der Basiszins des gewünschten Kalenderjahres hinterlegt ist. Das BMF veröffentlicht ihn jeweils zu Jahresbeginn im Bundessteuerblatt; noch offene Jahre sind gelb markiert.")
a(12, "Schritt 2", "Im Blatt 'Depot' oben das Steuerjahr und die Anlegerart eintragen. Die Anlegerart steuert den Teilfreistellungssatz.")
a(13, "Schritt 3", "Je Fondsposition eine Zeile ausfüllen: ISIN, Bezeichnung, Fondsart (Auswahlliste), Anteilsbestand zum 31.12., Rücknahmepreis am ersten und am letzten Bewertungstag des Jahres, Ausschüttungen je Anteil sowie – nur bei Erwerb im Steuerjahr – den Erwerbsmonat.")
a(14, "Schritt 4", "Ergebnis im Blatt 'Auswertung' ablesen. Dort ist auch der noch nicht ausgeschöpfte Freistellungsauftrag einzutragen.")
a(15, "Farblegende", "Gelb hinterlegt mit blauer Schrift = Eingabezelle. Grau = Berechnung, bitte nicht überschreiben. Grüne Schrift = Verweis auf ein anderes Blatt.")
a(16, "Beispielzeilen", "Die vier Zeilen im Blatt 'Depot' sind Musterdaten und können vollständig überschrieben werden. Zusätzliche Zeilen: Zeile innerhalb des Tabellenbereichs kopieren und einfügen, damit die Formeln erhalten bleiben.")

sec(18, "3. Rechenweg je Anteil")
a(19, "Basisertrag", "Rücknahmepreis am ersten Bewertungstag des Kalenderjahres  ×  Basiszins  ×  70 %   (§ 18 Abs. 2 Satz 1 InvStG)")
a(20, "Begrenzung", "Der Basisertrag ist auf den Mehrbetrag begrenzt: (Rücknahmepreis Jahresende – Rücknahmepreis Jahresanfang) + Ausschüttungen   (§ 18 Abs. 2 Satz 2 InvStG). In Verlustjahren beträgt die Vorabpauschale daher null.")
a(21, "Vorabpauschale", "begrenzter Basisertrag  –  Ausschüttungen des Kalenderjahres, mindestens null   (§ 18 Abs. 1 InvStG)")
a(22, "Erwerbsjahr", "Im Jahr des Erwerbs mindert sich die Vorabpauschale um ein Zwölftel für jeden vollen Monat vor dem Erwerbsmonat   (§ 18 Abs. 5 InvStG). Erwerb im April = Faktor 9/12.")
a(23, "Negativer Basiszins", "Ist der Basiszins null oder negativ (z. B. 2021 und 2022), fällt keine Vorabpauschale an.")
a(24, "Teilfreistellung", "Auf die Vorabpauschale wird die Teilfreistellung nach § 20 InvStG angewendet (Aktienfonds 30 %, Mischfonds 15 %, Immobilienfonds 60 %, Auslands-Immobilienfonds 80 % im Privatvermögen).")
a(25, "Zufluss", "Die Vorabpauschale gilt am ersten Werktag des folgenden Kalenderjahres als zugeflossen (§ 18 Abs. 4 InvStG) und wird erst dort besteuert.")

sec(27, "4. Wichtige Hinweise für die Praxis")
a(28, "Anteilsbestand", "Maßgeblich ist der Bestand zum Zuflusszeitpunkt. Unterjährig vollständig veräußerte Positionen lösen keine Vorabpauschale aus – sie gehören nicht in die Tabelle.")
a(29, "Ausschüttungen", "Nur Ausschüttungen des Kalenderjahres ansetzen, bei unterjährigem Erwerb nur die nach dem Erwerb vereinnahmten.")
a(30, "Rücknahmepreis", "Maßgeblich ist der Rücknahmepreis; wird keiner festgesetzt, tritt der Börsen- oder Marktpreis an seine Stelle (§ 18 Abs. 2 i. V. m. § 6 InvStG). Bei ETF ist das in der Regel der Schlusskurs bzw. NAV.")
a(31, "Steuerabzug", "Die depotführende Stelle zieht die Steuer vom Verrechnungskonto ein (§ 44 Abs. 1 Satz 11 EStG). Reicht die Deckung nicht aus, meldet die Bank den Betrag dem Finanzamt – auf ausreichende Liquidität im Januar achten.")
a(32, "Kirchensteuer", "Beim Steuerabzug mindert die Kirchensteuer die Bemessungsgrundlage der Kapitalertragsteuer; die Mappe rechnet mit KapESt = Ertrag × 25 % / (1 + 25 % × Kirchensteuersatz).")
a(33, "Betriebsvermögen", "Die Bank wendet beim Steuerabzug stets die Privatanlegersätze an. Die höheren Teilfreistellungssätze für Betriebsvermögen wirken erst in der Veranlagung.")
a(34, "Anschaffungskosten", "Versteuerte Vorabpauschalen mindern bei späterer Veräußerung den steuerpflichtigen Gewinn (§ 19 Abs. 1 Satz 4 InvStG) – außerhalb dieser Mappe fortzuschreiben.")

sec(36, "5. Haftungsausschluss")
a(37, "", "Diese Arbeitsmappe ist ein Berechnungshilfsmittel und ersetzt weder die Steuerbescheinigung der depotführenden Stelle noch eine Prüfung im Einzelfall. Rechtsstand: §§ 18, 20 InvStG in der Fassung ab 2018. Alle Stammdaten und Ergebnisse sind vor Verwendung zu verifizieren.", F_BASE, F_NOTE)
ws.row_dimensions[37].height = 30

for r in range(5, 38):
    ws.row_dimensions[r].height = max(ws.row_dimensions[r].height or 0, 14)

# ================================================================ 2 STAMMDATEN
sd = wb.create_sheet("Stammdaten")
sd.sheet_view.showGridLines = False
sd.column_dimensions["A"].width = 3
sd.column_dimensions["B"].width = 52
for c in "CDE":
    sd.column_dimensions[c].width = 22
sd.column_dimensions["F"].width = 60

sd["B2"] = "Stammdaten"
sd["B2"].font = F_TITLE

def sdsec(row, text, last_col=6):
    for col in range(2, last_col + 1):
        sd.cell(row=row, column=col).fill = FILL_SEC
    sd.cell(row=row, column=2, value=text).font = F_SEC

# --- Basiszins
sdsec(4, "1. Basiszins nach § 18 Abs. 3 InvStG")
for col, txt in ((2, "Kalenderjahr"), (3, "Basiszins"), (4, "davon 70 % (Faktor Basisertrag)"), (5, "Status"), (6, "Hinweis")):
    c = sd.cell(row=5, column=col, value=txt)
    c.font = F_HDR
    c.fill = FILL_HDR
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
sd.row_dimensions[5].height = 30

BASISZINS = [
    (2018, 0.0087, "veröffentlicht", ""),
    (2019, 0.0052, "veröffentlicht", ""),
    (2020, 0.0007, "veröffentlicht", ""),
    (2021, -0.0045, "veröffentlicht", "negativer Basiszins – keine Vorabpauschale"),
    (2022, -0.0005, "veröffentlicht", "negativer Basiszins – keine Vorabpauschale"),
    (2023, 0.0255, "veröffentlicht", ""),
    (2024, 0.0229, "veröffentlicht", ""),
    (2025, 0.0253, "veröffentlicht", ""),
    (2026, None, "bitte eintragen", "BMF-Veröffentlichung im Bundessteuerblatt abwarten bzw. nachtragen"),
    (2027, None, "bitte eintragen", "BMF-Veröffentlichung im Bundessteuerblatt abwarten bzw. nachtragen"),
]
BZ_FIRST, BZ_LAST = 6, 6 + len(BASISZINS) - 1
for i, (jahr, zins, status, hinweis) in enumerate(BASISZINS):
    r = BZ_FIRST + i
    cj = sd.cell(row=r, column=2, value=jahr)
    cj.number_format = "0"
    cj.font = F_BASE
    cz = sd.cell(row=r, column=3)
    cz.number_format = PCT
    if zins is None:
        cz.fill = FILL_IN
        cz.font = F_IN
    else:
        cz.value = zins
        cz.font = F_IN
    cd = sd.cell(row=r, column=4, value=f"=IF(C{r}=\"\",\"\",C{r}*$C${BZ_LAST + 3})")
    cd.number_format = PCT
    cd.font = F_BASE
    cd.fill = FILL_CALC
    sd.cell(row=r, column=5, value=status).font = F_BASE
    sd.cell(row=r, column=6, value=hinweis).font = F_NOTE
    for col in range(2, 7):
        sd.cell(row=r, column=col).border = BOX

FAKTOR_ROW = BZ_LAST + 3          # 18
sd.cell(row=FAKTOR_ROW, column=2, value="Faktor Basisertrag (§ 18 Abs. 2 Satz 1 InvStG)").font = F_BOLD
fk = sd.cell(row=FAKTOR_ROW, column=3, value=0.70)
fk.number_format = PCT0
fk.font = F_IN
fk.fill = FILL_IN
sd.cell(row=FAKTOR_ROW, column=6,
        value="Gesetzlich festgeschrieben; nur bei Gesetzesänderung anpassen.").font = F_NOTE
sd.cell(row=FAKTOR_ROW + 1, column=2,
        value="Quelle Basiszins: jährliches BMF-Schreiben, veröffentlicht im Bundessteuerblatt Teil I. Werte vor Übernahme in die Beratung verifizieren.").font = F_NOTE

# --- Teilfreistellung
TF_SEC = FAKTOR_ROW + 3           # 21
TF_HDR = TF_SEC + 1               # 22
TF_FIRST = TF_HDR + 1             # 23
sdsec(TF_SEC, "2. Teilfreistellungssätze nach § 20 InvStG")
for col, txt in ((2, "Fondsart"), (3, "Privatvermögen"), (4, "Betriebsvermögen (Einkommensteuer)"),
                 (5, "Betriebsvermögen (Körperschaftsteuer)"), (6, "Voraussetzung")):
    c = sd.cell(row=TF_HDR, column=col, value=txt)
    c.font = F_HDR
    c.fill = FILL_HDR
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
sd.row_dimensions[TF_HDR].height = 32

TEILFREI = [
    ("Aktienfonds", 0.30, 0.60, 0.80, "fortlaufend mind. 51 % Kapitalbeteiligungen (§ 2 Abs. 6 InvStG)"),
    ("Mischfonds", 0.15, 0.30, 0.40, "fortlaufend mind. 25 % Kapitalbeteiligungen"),
    ("Immobilienfonds", 0.60, 0.60, 0.60, "fortlaufend mind. 51 % Immobilien und Immobiliengesellschaften"),
    ("Auslands-Immobilienfonds", 0.80, 0.80, 0.80, "fortlaufend mind. 51 % ausländische Immobilien und Immobiliengesellschaften"),
    ("Sonstiger Fonds", 0.00, 0.00, 0.00, "keine Teilfreistellung (z. B. Renten- und Geldmarktfonds)"),
]
TF_LAST = TF_FIRST + len(TEILFREI) - 1
for i, (art, pv, est, kst, vor) in enumerate(TEILFREI):
    r = TF_FIRST + i
    sd.cell(row=r, column=2, value=art).font = F_BASE
    for col, val in ((3, pv), (4, est), (5, kst)):
        c = sd.cell(row=r, column=col, value=val)
        c.number_format = PCT0
        c.font = F_BASE
        c.alignment = Alignment(horizontal="center")
    sd.cell(row=r, column=6, value=vor).font = F_NOTE
    for col in range(2, 7):
        sd.cell(row=r, column=col).border = BOX
sd.cell(row=TF_LAST + 1, column=2,
        value="Die depotführende Stelle wendet beim Kapitalertragsteuerabzug immer die Privatanlegersätze an; abweichende Betriebsvermögenssätze wirken erst in der Veranlagung.").font = F_NOTE

# --- Steuersaetze
ST_SEC = TF_LAST + 3              # 31
sdsec(ST_SEC, "3. Steuersätze und Freibeträge")
KAPST_ROW = ST_SEC + 1
SOLZ_ROW = ST_SEC + 2
KIST_ROW = ST_SEC + 3
SPB1_ROW = ST_SEC + 4
SPB2_ROW = ST_SEC + 5
STEUER = [
    (KAPST_ROW, "Kapitalertragsteuer (§ 43a Abs. 1 EStG)", 0.25, PCT0, False, ""),
    (SOLZ_ROW, "Solidaritätszuschlag auf die Kapitalertragsteuer", 0.055, PCT0, False,
     "Für den Steuerabzug auf Kapitalerträge unverändert zu erheben."),
    (KIST_ROW, "Kirchensteuersatz (0 % / 8 % / 9 %)", 0.00, PCT0, True,
     "8 % in Bayern und Baden-Württemberg, sonst 9 %; 0 % ohne Kirchensteuerpflicht."),
    (SPB1_ROW, "Sparer-Pauschbetrag Einzelveranlagung", 1000, EUR, False, "seit 2023"),
    (SPB2_ROW, "Sparer-Pauschbetrag Zusammenveranlagung", 2000, EUR, False, "seit 2023"),
]
for r, label, val, fmt, is_input, note in STEUER:
    sd.cell(row=r, column=2, value=label).font = F_BASE
    c = sd.cell(row=r, column=3, value=val)
    c.number_format = fmt
    c.font = F_IN
    if is_input:
        c.fill = FILL_IN
    if note:
        sd.cell(row=r, column=6, value=note).font = F_NOTE
    for col in range(2, 4):
        sd.cell(row=r, column=col).border = BOX

# --- Anlegerart-Liste (fuer Auswahlliste im Blatt Depot)
AL_ROW = SPB2_ROW + 3
sd.cell(row=AL_ROW, column=2, value="4. Auswahlliste Anlegerart").font = F_SEC
ANLEGERARTEN = ["Privatvermögen", "Betriebsvermögen (Einkommensteuer)", "Betriebsvermögen (Körperschaftsteuer)"]
for i, art in enumerate(ANLEGERARTEN):
    sd.cell(row=AL_ROW + 1 + i, column=2, value=art).font = F_BASE
AL_FIRST, AL_LAST = AL_ROW + 1, AL_ROW + len(ANLEGERARTEN)

dv_kist = DataValidation(type="list", formula1='"0%,8%,9%"', allow_blank=False)
sd.add_data_validation(dv_kist)
dv_kist.add(sd.cell(row=KIST_ROW, column=3))

# ===================================================================== 3 DEPOT
dp = wb.create_sheet("Depot")
dp.sheet_view.showGridLines = False

dp["B2"] = "Depot – Ermittlung der Vorabpauschale je Fondsposition"
dp["B2"].font = F_TITLE

PARAMS = [
    (4, "Steuerjahr", 2025, "0", True, None),
    (5, "Basiszins laut Stammdaten", None, PCT, False,
     f"=IFERROR(INDEX(Stammdaten!$C${BZ_FIRST}:$C${BZ_LAST},MATCH($D$4,Stammdaten!$B${BZ_FIRST}:$B${BZ_LAST},0)),0)"),
    (6, "davon 70 % (Faktor Basisertrag)", None, PCT, False, f"=$D$5*Stammdaten!$C${FAKTOR_ROW}"),
    (7, "Anlegerart (steuert die Teilfreistellung)", "Privatvermögen", None, True, None),
]
for row, label, val, fmt, is_input, formula in PARAMS:
    dp.cell(row=row, column=2, value=label).font = F_BOLD
    c = dp.cell(row=row, column=4)
    if formula:
        c.value = formula
        c.font = F_LINK
        c.fill = FILL_CALC
    else:
        c.value = val
        c.font = F_IN
        c.fill = FILL_IN
    if fmt:
        c.number_format = fmt
    c.alignment = Alignment(horizontal="center")
    c.border = BOX

dp["F4"] = (f'=IF(ISNA(MATCH($D$4,Stammdaten!$B${BZ_FIRST}:$B${BZ_LAST},0)),'
            f'"Achtung: Steuerjahr ist in den Stammdaten nicht angelegt.",'
            f'IF(COUNT(INDEX(Stammdaten!$C${BZ_FIRST}:$C${BZ_LAST},MATCH($D$4,Stammdaten!$B${BZ_FIRST}:$B${BZ_LAST},0)))=0,'
            f'"Achtung: Basiszins fuer dieses Jahr noch nicht hinterlegt – bitte in den Stammdaten eintragen.",'
            f'IF($D$5<=0,"Hinweis: Basiszins ist null oder negativ – fuer dieses Jahr faellt keine Vorabpauschale an.","")))')
dp["F4"].font = F_WARN

dp["F6"] = ('="Zufluss der Vorabpauschale: erster Werktag des Jahres "&TEXT($D$4+1,"0")'
            '&" (§ 18 Abs. 4 InvStG)"')
dp["F6"].font = F_NOTE

HEADERS = [
    ("A", "Nr.", 5, None),
    ("B", "ISIN / WKN", 15, None),
    ("C", "Fondsbezeichnung", 34, None),
    ("D", "Fondsart (§ 20 InvStG)", 24, None),
    ("E", "Anteile am 31.12. (Stück)", 12, STK),
    ("F", "Rücknahmepreis 1. Bewertungstag (€ / Anteil)", 14, EUR),
    ("G", "Rücknahmepreis letzter Bewertungstag (€ / Anteil)", 14, EUR),
    ("H", "Ausschüttungen im Jahr (€ / Anteil)", 13, EUR),
    ("I", "Erwerbsmonat im Steuerjahr (1–12; leer = früher)", 12, "0"),
    ("J", "Monatsfaktor (§ 18 Abs. 5)", 10, "0.0000"),
    ("K", "Basisertrag je Anteil", 13, EUR4),
    ("L", "Mehrbetrag je Anteil (Grenze)", 13, EUR4),
    ("M", "Begrenzter Basisertrag je Anteil", 13, EUR4),
    ("N", "Vorabpauschale je Anteil", 13, EUR4),
    ("O", "Vorabpauschale gesamt", 15, EUR),
    ("P", "Teilfreistellung", 11, PCT0),
    ("Q", "Teilfreistellungsbetrag", 15, EUR),
    ("R", "Steuerpflichtiger Ertrag", 15, EUR),
]
HDR_ROW = 8
for col_letter, title, width, _fmt in HEADERS:
    dp.column_dimensions[col_letter].width = width
    c = dp[f"{col_letter}{HDR_ROW}"]
    c.value = title
    c.font = F_HDR
    c.fill = FILL_HDR
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BOX
dp.row_dimensions[HDR_ROW].height = 58

BEISPIELE = [
    ("IE00B4L5Y983", "iShares Core MSCI World UCITS ETF (thesaurierend)", "Aktienfonds", 250, 88.50, 101.20, 0.00, None),
    ("DE0008474503", "DWS Top Dividende (ausschüttend)", "Aktienfonds", 400, 138.00, 145.50, 3.60, None),
    ("DE0009807016", "hausInvest (offener Immobilienfonds)", "Immobilienfonds", 300, 43.20, 43.80, 0.35, 4),
    ("LU0323578657", "Flossbach von Storch Multiple Opportunities", "Mischfonds", 100, 320.00, 321.00, 0.00, None),
]

INPUT_COLS = "BCDEFGHI"
CALC_COLS = "JKLMNOPQR"

for r in range(FIRST_ROW, LAST_ROW + 1):
    idx = r - FIRST_ROW
    nr = dp.cell(row=r, column=1, value=f'=IF($C{r}="","",ROW()-{FIRST_ROW - 1})')
    nr.font = F_BASE
    nr.alignment = Alignment(horizontal="center")

    if idx < len(BEISPIELE):
        isin, name, art, anteile, rp1, rp2, aus, monat = BEISPIELE[idx]
        dp[f"B{r}"] = isin
        dp[f"C{r}"] = name
        dp[f"D{r}"] = art
        dp[f"E{r}"] = anteile
        dp[f"F{r}"] = rp1
        dp[f"G{r}"] = rp2
        dp[f"H{r}"] = aus
        if monat is not None:
            dp[f"I{r}"] = monat

    for col_letter in INPUT_COLS:
        c = dp[f"{col_letter}{r}"]
        c.font = F_IN
        c.fill = FILL_IN
        c.border = BOX
        fmt = dict((h[0], h[3]) for h in HEADERS)[col_letter]
        if fmt:
            c.number_format = fmt

    formulas = {
        "J": f'=IF($C{r}="","",IF($I{r}="",1,MAX(0,(13-$I{r})/12)))',
        "K": f'=IF($C{r}="","",MAX(0,$F{r}*$D$6))',
        "L": f'=IF($C{r}="","",MAX(0,($G{r}-$F{r})+$H{r}))',
        "M": f'=IF($C{r}="","",MIN($K{r},$L{r}))',
        "N": f'=IF($C{r}="","",MAX(0,$M{r}-$H{r})*$J{r})',
        "O": f'=IF($C{r}="","",$N{r}*$E{r})',
        "P": (f'=IF($C{r}="","",IFERROR(INDEX(Stammdaten!$C${TF_FIRST}:$E${TF_LAST},'
              f'MATCH($D{r},Stammdaten!$B${TF_FIRST}:$B${TF_LAST},0),'
              f'MATCH($D$7,Stammdaten!$C${TF_HDR}:$E${TF_HDR},0)),0))'),
        "Q": f'=IF($C{r}="","",$O{r}*$P{r})',
        "R": f'=IF($C{r}="","",$O{r}-$Q{r})',
    }
    for col_letter in CALC_COLS:
        c = dp[f"{col_letter}{r}"]
        c.value = formulas[col_letter]
        c.font = F_BASE
        c.fill = FILL_CALC
        c.border = BOX
        fmt = dict((h[0], h[3]) for h in HEADERS)[col_letter]
        if fmt:
            c.number_format = fmt

# Summenzeile
dp.cell(row=SUM_ROW, column=3, value="Summe Depot").font = F_BOLD
for col_letter in ("O", "Q", "R"):
    c = dp[f"{col_letter}{SUM_ROW}"]
    c.value = f"=SUM({col_letter}{FIRST_ROW}:{col_letter}{LAST_ROW})"
    c.number_format = EUR
    c.font = F_BOLD
for col in range(1, 19):
    cell = dp.cell(row=SUM_ROW, column=col)
    cell.fill = FILL_SUM
    cell.border = BOX

dp.cell(row=SUM_ROW + 2, column=2,
        value="Spalten B bis I sind Eingabespalten (gelb), Spalten J bis R rechnen automatisch. Die vier vorbelegten Zeilen sind Beispieldaten und können überschrieben werden.").font = F_NOTE
dp.cell(row=SUM_ROW + 3, column=2,
        value="Mehrbetrag je Anteil = (Rücknahmepreis Jahresende – Rücknahmepreis Jahresanfang) + Ausschüttungen; er begrenzt den Basisertrag nach § 18 Abs. 2 Satz 2 InvStG.").font = F_NOTE
dp.cell(row=SUM_ROW + 4, column=2,
        value="Unterjährig vollständig veräußerte Positionen lösen keine Vorabpauschale aus und gehören nicht in diese Tabelle.").font = F_NOTE

dv_art = DataValidation(type="list", formula1=f"=Stammdaten!$B${TF_FIRST}:$B${TF_LAST}", allow_blank=True)
dv_art.error = "Bitte eine Fondsart aus der Liste wählen."
dv_art.errorTitle = "Ungültige Fondsart"
dp.add_data_validation(dv_art)
dv_art.add(f"D{FIRST_ROW}:D{LAST_ROW}")

dv_monat = DataValidation(type="whole", operator="between", formula1=1, formula2=12, allow_blank=True)
dv_monat.error = "Erwerbsmonat als ganze Zahl 1 bis 12 eintragen; bei Erwerb vor dem Steuerjahr leer lassen."
dv_monat.errorTitle = "Ungültiger Erwerbsmonat"
dp.add_data_validation(dv_monat)
dv_monat.add(f"I{FIRST_ROW}:I{LAST_ROW}")

dv_anleger = DataValidation(type="list", formula1=f"=Stammdaten!$B${AL_FIRST}:$B${AL_LAST}", allow_blank=False)
dp.add_data_validation(dv_anleger)
dv_anleger.add("D7")

dv_jahr = DataValidation(type="list", formula1=f"=Stammdaten!$B${BZ_FIRST}:$B${BZ_LAST}", allow_blank=False)
dp.add_data_validation(dv_jahr)
dv_jahr.add("D4")

dp.freeze_panes = f"E{FIRST_ROW}"
dp.page_setup.orientation = "landscape"
dp.page_setup.fitToWidth = 1
dp.page_setup.fitToHeight = 0
dp.sheet_properties.pageSetUpPr.fitToPage = True

# ================================================================ 4 AUSWERTUNG
aw = wb.create_sheet("Auswertung")
aw.sheet_view.showGridLines = False
aw.column_dimensions["A"].width = 3
aw.column_dimensions["B"].width = 62
aw.column_dimensions["C"].width = 20
aw.column_dimensions["D"].width = 18
aw.column_dimensions["E"].width = 18
aw.column_dimensions["F"].width = 18
aw.column_dimensions["G"].width = 52

aw["B2"] = "Auswertung – Vorabpauschale und Steuerabzug"
aw["B2"].font = F_TITLE

def awsec(row, text, last_col=7):
    for col in range(2, last_col + 1):
        aw.cell(row=row, column=col).fill = FILL_SEC
    aw.cell(row=row, column=2, value=text).font = F_SEC

def awline(row, label, formula, fmt=EUR, font=F_BASE, note="", is_input=False):
    aw.cell(row=row, column=2, value=label).font = font
    c = aw.cell(row=row, column=3, value=formula)
    if fmt:
        c.number_format = fmt
    c.font = F_IN if is_input else font
    if is_input:
        c.fill = FILL_IN
    c.border = BOX
    if note:
        aw.cell(row=row, column=7, value=note).font = F_NOTE
    return c

awsec(4, "Rahmendaten")
awline(5, "Steuerjahr", "=Depot!$D$4", "0", F_BASE).font = F_LINK
awline(6, "Basiszins", "=Depot!$D$5", PCT, F_BASE).font = F_LINK
awline(7, "Anlegerart", "=Depot!$D$7", None, F_BASE).font = F_LINK
awline(8, "Zufluss der Vorabpauschale", '=WORKDAY(DATE($C$5+1,1,1)-1,1)', "DD.MM.YYYY", F_BASE,
       "Erster Werktag des Folgejahres (§ 18 Abs. 4 InvStG); gesetzliche Feiertage sind nicht berücksichtigt.")

awsec(10, "A. Steuerpflichtiger Ertrag")
awline(11, "Summe Vorabpauschalen (brutto)", f"=SUM(Depot!$O${FIRST_ROW}:$O${LAST_ROW})", EUR, F_BASE).font = F_LINK
awline(12, "abzüglich Teilfreistellung (§ 20 InvStG)", f"=-SUM(Depot!$Q${FIRST_ROW}:$Q${LAST_ROW})", EUR, F_BASE).font = F_LINK
awline(13, "Steuerpflichtiger Kapitalertrag", "=C11+C12", EUR, F_BOLD)
awline(14, "Noch nicht ausgeschöpfter Freistellungsauftrag für dieses Depot", 0, EUR, F_BASE,
       f"Sparer-Pauschbetrag: {int(STEUER[3][2]):,} € Einzel- / {int(STEUER[4][2]):,} € Zusammenveranlagung (Stammdaten). Nur den noch freien Restbetrag eintragen.".replace(",", "."),
       is_input=True)
awline(15, "davon anrechenbar", "=-MIN($C$14,MAX(0,$C$13))", EUR, F_BASE)
awline(16, "Bemessungsgrundlage für den Steuerabzug", "=MAX(0,$C$13+$C$15)", EUR, F_BOLD)

awsec(18, "B. Steuerabzug durch die depotführende Stelle")
awline(19, "Kirchensteuersatz", f"=Stammdaten!$C${KIST_ROW}", PCT0, F_BASE,
       "Änderung im Blatt 'Stammdaten'.").font = F_LINK
awline(20, "Kapitalertragsteuer", f"=$C$16*Stammdaten!$C${KAPST_ROW}/(1+Stammdaten!$C${KAPST_ROW}*$C$19)", EUR, F_BASE,
       "25 %; bei Kirchensteuerpflicht gemindert um den Sonderausgabeneffekt (§ 32d Abs. 1 Satz 3 EStG).")
awline(21, "Solidaritätszuschlag", f"=$C$20*Stammdaten!$C${SOLZ_ROW}", EUR, F_BASE)
awline(22, "Kirchensteuer", "=$C$20*$C$19", EUR, F_BASE)
awline(23, "Gesamte Steuerbelastung", "=SUM($C$20:$C$22)", EUR, F_BOLD)
aw.cell(row=23, column=3).fill = FILL_SUM
awline(24, "Belastung bezogen auf die Bruttovorabpauschale", '=IF($C$11=0,0,$C$23/$C$11)', PCT, F_BASE)
awline(25, "Erforderliche Deckung auf dem Verrechnungskonto", "=$C$23", EUR, F_BASE,
       "Einzug durch die Bank zu Jahresbeginn (§ 44 Abs. 1 Satz 11 EStG); bei fehlender Deckung Meldung an das Finanzamt.")

awsec(27, "C. Aufteilung nach Fondsarten")
for col, txt in ((2, "Fondsart"), (3, "Positionen"), (4, "Vorabpauschale brutto"),
                 (5, "Teilfreistellung"), (6, "Steuerpflichtiger Ertrag")):
    c = aw.cell(row=28, column=col, value=txt)
    c.font = F_HDR
    c.fill = FILL_HDR
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BOX
aw.row_dimensions[28].height = 30

for i in range(len(TEILFREI)):
    r = 29 + i
    src = TF_FIRST + i
    aw.cell(row=r, column=2, value=f"=Stammdaten!$B${src}").font = F_LINK
    aw.cell(row=r, column=3,
            value=f'=COUNTIFS(Depot!$D${FIRST_ROW}:$D${LAST_ROW},$B{r},Depot!$C${FIRST_ROW}:$C${LAST_ROW},"<>")').number_format = "0"
    aw.cell(row=r, column=4,
            value=f"=SUMIF(Depot!$D${FIRST_ROW}:$D${LAST_ROW},$B{r},Depot!$O${FIRST_ROW}:$O${LAST_ROW})").number_format = EUR
    aw.cell(row=r, column=5,
            value=f"=SUMIF(Depot!$D${FIRST_ROW}:$D${LAST_ROW},$B{r},Depot!$Q${FIRST_ROW}:$Q${LAST_ROW})").number_format = EUR
    aw.cell(row=r, column=6,
            value=f"=SUMIF(Depot!$D${FIRST_ROW}:$D${LAST_ROW},$B{r},Depot!$R${FIRST_ROW}:$R${LAST_ROW})").number_format = EUR
    for col in range(2, 7):
        cell = aw.cell(row=r, column=col)
        cell.border = BOX
        if col > 2:
            cell.font = F_BASE

TOTAL_ROW = 29 + len(TEILFREI)
aw.cell(row=TOTAL_ROW, column=2, value="Summe").font = F_BOLD
for col in (3, 4, 5, 6):
    L = get_column_letter(col)
    c = aw.cell(row=TOTAL_ROW, column=col, value=f"=SUM({L}29:{L}{TOTAL_ROW - 1})")
    c.number_format = "0" if col == 3 else EUR
    c.font = F_BOLD
for col in range(2, 7):
    cell = aw.cell(row=TOTAL_ROW, column=col)
    cell.fill = FILL_SUM
    cell.border = BOX

NOTE_ROW = TOTAL_ROW + 2
awsec(NOTE_ROW, "D. Hinweise")
NOTES = [
    "Die Vorabpauschale gilt am ersten Werktag des Folgejahres als zugeflossen und wird erst in diesem Jahr besteuert.",
    "Versteuerte Vorabpauschalen mindern bei späterer Veräußerung den steuerpflichtigen Gewinn (§ 19 Abs. 1 Satz 4 InvStG) und sind gesondert fortzuschreiben.",
    "Beim Steuerabzug wendet die Bank stets die Teilfreistellungssätze für Privatanleger an; abweichende Sätze im Betriebsvermögen wirken erst in der Veranlagung.",
    "Die Berechnung ersetzt nicht die Steuerbescheinigung der depotführenden Stelle; Abweichungen sind im Einzelfall zu klären.",
]
for i, note in enumerate(NOTES):
    aw.cell(row=NOTE_ROW + 1 + i, column=2, value="• " + note).font = F_NOTE

aw.page_setup.orientation = "portrait"
aw.page_setup.fitToWidth = 1
aw.page_setup.fitToHeight = 0
aw.sheet_properties.pageSetUpPr.fitToPage = True

wb.active = 0
wb.save(OUT)
print("geschrieben:", OUT)
