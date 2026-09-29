(function (root) {
  'use strict';

  // Persönliche Freibeträge (§ 16 ErbStG) und Steuerklassen (§ 15 ErbStG)
  const BEZIEHUNGEN = {
    ehegatte:        { label: 'Ehegatte / eingetragener Lebenspartner', stkl: 1, freibetrag: 500000 },
    kind:            { label: 'Kind / Stiefkind', stkl: 1, freibetrag: 400000 },
    enkel_verst:     { label: 'Enkel (Elternteil bereits verstorben)', stkl: 1, freibetrag: 400000 },
    enkel:           { label: 'Enkel', stkl: 1, freibetrag: 200000 },
    urenkel:         { label: 'Urenkel', stkl: 1, freibetrag: 100000 },
    eltern:          { label: 'Eltern / Großeltern', stkl: 1, freibetrag: 100000, schenkung: { stkl: 2, freibetrag: 20000 } },
    geschwister:     { label: 'Geschwister', stkl: 2, freibetrag: 20000 },
    nichte:          { label: 'Nichte / Neffe', stkl: 2, freibetrag: 20000 },
    schwieger:       { label: 'Schwiegerkind / Schwiegereltern', stkl: 2, freibetrag: 20000 },
    stiefeltern:     { label: 'Stiefeltern', stkl: 2, freibetrag: 20000 },
    geschieden:      { label: 'Geschiedener Ehegatte', stkl: 2, freibetrag: 20000 },
    lebensgefaehrte: { label: 'Lebensgefährte (nicht verheiratet)', stkl: 3, freibetrag: 20000 },
    sonstige:        { label: 'Sonstige Person / nicht verwandt', stkl: 3, freibetrag: 20000 }
  };

  // Steuersätze (§ 19 Abs. 1 ErbStG) in Prozent je Steuerklasse I, II, III
  const TARIF = [
    { bis: 75000,    saetze: [7, 15, 30] },
    { bis: 300000,   saetze: [11, 20, 30] },
    { bis: 600000,   saetze: [15, 25, 30] },
    { bis: 6000000,  saetze: [19, 30, 30] },
    { bis: 13000000, saetze: [23, 35, 50] },
    { bis: 26000000, saetze: [27, 40, 50] },
    { bis: Infinity, saetze: [30, 43, 50] }
  ];

  // Besonderer Versorgungsfreibetrag für Kinder nach Alter (§ 17 Abs. 2 ErbStG)
  const VERSORGUNG_KIND = [
    { bisAlter: 5, betrag: 52000 },
    { bisAlter: 10, betrag: 41000 },
    { bisAlter: 15, betrag: 30700 },
    { bisAlter: 20, betrag: 20500 },
    { bisAlter: 27, betrag: 10300 }
  ];

  const ERBFALLKOSTEN_PAUSCHALE = 15000;
  const PFLEGEFREIBETRAG = 20000;

  function stufeIndex(erwerb) {
    return TARIF.findIndex(s => erwerb <= s.bis);
  }

  // Tarifsteuer mit Härteausgleich (§ 19 Abs. 3 ErbStG)
  function tarifsteuer(erwerb, stkl) {
    if (erwerb <= 0) return { steuer: 0, satz: TARIF[0].saetze[stkl - 1], stufe: 0, haerteausgleich: false };
    const i = stufeIndex(erwerb);
    const satz = TARIF[i].saetze[stkl - 1];
    const normal = Math.floor(erwerb * satz / 100);
    if (i === 0) return { steuer: normal, satz, stufe: i, haerteausgleich: false };
    const grenze = TARIF[i - 1].bis;
    const vorSatz = TARIF[i - 1].saetze[stkl - 1];
    const faktor = satz <= 30 ? 0.5 : 0.75;
    const begrenzt = Math.floor(grenze * vorSatz / 100 + faktor * (erwerb - grenze));
    return begrenzt < normal
      ? { steuer: begrenzt, satz, stufe: i, haerteausgleich: true }
      : { steuer: normal, satz, stufe: i, haerteausgleich: false };
  }

  function abrunden100(betrag) {
    return Math.max(0, Math.floor(betrag / 100) * 100);
  }

  function versorgungsfreibetrag(e, beziehung) {
    if (e.art !== 'erbschaft') return 0;
    let basis = 0;
    if (beziehung === 'ehegatte') basis = 256000;
    if (beziehung === 'kind' || beziehung === 'enkel_verst') {
      const stufe = VERSORGUNG_KIND.find(s => e.alterKind <= s.bisAlter);
      basis = stufe ? stufe.betrag : 0;
    }
    return Math.max(0, basis - (e.versorgungsbezuege || 0));
  }

  function berechne(e) {
    const b = BEZIEHUNGEN[e.beziehung];
    const klasse = e.art === 'schenkung' && b.schenkung ? b.schenkung : b;
    const stkl = klasse.stkl;
    const q = e.art === 'erbschaft' ? Math.min(Math.max(e.quote, 0), 100) / 100 : 1;
    const zeilen = [];

    const anteil = x => (x || 0) * q;
    const brutto = anteil(e.bank) + anteil(e.wertpapiere) + anteil(e.immobilien) +
      anteil(e.vermietet) + anteil(e.familienheim) + anteil(e.hausrat) +
      anteil(e.beweglich) + anteil(e.sonstiges);
    zeilen.push({ text: 'Wert des Erwerbs', ref: q < 1 ? `Anteil ${(q * 100).toLocaleString('de-DE')} %` : '', betrag: brutto });

    // Sachliche Steuerbefreiungen
    let hausratFrei, beweglichFrei;
    if (stkl === 1) {
      hausratFrei = Math.min(anteil(e.hausrat), 41000);
      beweglichFrei = Math.min(anteil(e.beweglich), 12000);
    } else {
      hausratFrei = Math.min(anteil(e.hausrat) + anteil(e.beweglich), 12000);
      beweglichFrei = 0;
    }
    if (hausratFrei + beweglichFrei > 0) {
      zeilen.push({ text: 'Freibetrag Hausrat und bewegliche Gegenstände', ref: '§ 13 Abs. 1 Nr. 1', betrag: -(hausratFrei + beweglichFrei) });
    }

    let heimFrei = 0;
    const heim = anteil(e.familienheim);
    if (heim > 0 && e.selbstgenutzt) {
      if (e.beziehung === 'ehegatte') {
        heimFrei = heim;
        zeilen.push({ text: 'Familienheim an Ehegatten', ref: e.art === 'erbschaft' ? '§ 13 Abs. 1 Nr. 4b' : '§ 13 Abs. 1 Nr. 4a', betrag: -heimFrei });
      } else if (e.art === 'erbschaft' && (e.beziehung === 'kind' || e.beziehung === 'enkel_verst')) {
        const flaeche = e.wohnflaeche > 0 ? e.wohnflaeche : 0;
        heimFrei = flaeche > 200 ? heim * 200 / flaeche : heim;
        zeilen.push({ text: flaeche > 200 ? `Familienheim an Kind (200 von ${flaeche} m² befreit)` : 'Familienheim an Kind', ref: '§ 13 Abs. 1 Nr. 4c', betrag: -heimFrei });
      }
    }

    const vermietAbschlag = anteil(e.vermietet) * 0.1;
    if (vermietAbschlag > 0) {
      zeilen.push({ text: 'Abschlag vermietete Wohnimmobilie (10 %)', ref: '§ 13d', betrag: -vermietAbschlag });
    }

    const pflege = e.art === 'erbschaft' && e.pflege ? PFLEGEFREIBETRAG : 0;
    if (pflege) zeilen.push({ text: 'Pflegefreibetrag', ref: '§ 13 Abs. 1 Nr. 9', betrag: -pflege });

    // Nachlassverbindlichkeiten
    const schulden = anteil(e.schulden);
    if (schulden > 0) zeilen.push({ text: 'Schulden', ref: '§ 10 Abs. 5 Nr. 1', betrag: -schulden });
    let kosten = 0;
    if (e.art === 'erbschaft') {
      const hoeher = (e.kosten || 0) > ERBFALLKOSTEN_PAUSCHALE;
      kosten = anteil(hoeher ? e.kosten : ERBFALLKOSTEN_PAUSCHALE);
      zeilen.push({ text: hoeher ? 'Nachgewiesene Erbfallkosten' : 'Erbfallkostenpauschale', ref: '§ 10 Abs. 5 Nr. 3', betrag: -kosten });
    }

    const befreiungen = hausratFrei + beweglichFrei + heimFrei + vermietAbschlag + pflege;
    const bereicherung = Math.max(0, brutto - befreiungen - schulden - kosten);
    zeilen.push({ text: 'Bereicherung', ref: '§ 10 Abs. 1', betrag: bereicherung, summe: true });

    const vorerwerb = e.vorerwerb || 0;
    if (vorerwerb > 0) zeilen.push({ text: 'Vorerwerbe der letzten 10 Jahre', ref: '§ 14', betrag: vorerwerb });

    const freibetrag = klasse.freibetrag;
    zeilen.push({ text: 'Persönlicher Freibetrag', ref: '§ 16', betrag: -Math.min(freibetrag, bereicherung + vorerwerb) });

    const versorgung = versorgungsfreibetrag(e, e.beziehung);
    const restNachFreibetrag = Math.max(0, bereicherung + vorerwerb - freibetrag);
    if (versorgung > 0) {
      zeilen.push({ text: 'Versorgungsfreibetrag', ref: '§ 17', betrag: -Math.min(versorgung, restNachFreibetrag) });
    }

    const stpflErwerb = abrunden100(restNachFreibetrag - versorgung);
    zeilen.push({ text: 'Steuerpflichtiger Erwerb', ref: 'auf volle 100 € abgerundet', betrag: stpflErwerb, summe: true });

    const tarif = tarifsteuer(stpflErwerb, stkl);
    let steuer = tarif.steuer;
    zeilen.push({
      text: `Steuer (${tarif.satz} %, Steuerklasse ${'I'.repeat(stkl)})`,
      ref: tarif.haerteausgleich ? '§ 19, mit Härteausgleich' : '§ 19',
      betrag: tarif.steuer
    });

    if (vorerwerb > 0) {
      const fiktiv = tarifsteuer(abrunden100(vorerwerb - freibetrag), stkl).steuer;
      const abzug = Math.max(fiktiv, e.vorsteuer || 0);
      const allein = tarifsteuer(abrunden100(bereicherung - freibetrag - versorgung), stkl).steuer;
      if (abzug > 0) zeilen.push({ text: 'Abzug Steuer auf Vorerwerbe', ref: '§ 14 Abs. 1', betrag: -Math.min(abzug, steuer) });
      steuer = Math.max(0, steuer - abzug, allein);
      if (steuer === allein && allein > tarif.steuer - abzug) {
        zeilen.push({ text: 'Mindeststeuer für den letzten Erwerb', ref: '§ 14 Abs. 1 S. 4', betrag: steuer - Math.max(0, tarif.steuer - abzug) });
      }
    }

    return {
      stkl,
      freibetrag,
      versorgung,
      bereicherung,
      stpflErwerb,
      satz: tarif.satz,
      stufe: tarif.stufe,
      haerteausgleich: tarif.haerteausgleich,
      steuer,
      netto: bereicherung - steuer,
      effektiv: bereicherung > 0 ? steuer / bereicherung * 100 : 0,
      zeilen
    };
  }

  const api = { BEZIEHUNGEN, TARIF, tarifsteuer, berechne };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Erbst = api;
})(this);
