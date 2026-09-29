(function () {
  'use strict';

  const { BEZIEHUNGEN, TARIF, berechne } = window.Erbst;
  const $ = id => document.getElementById(id);
  const euro = new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  const zahl = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 });
  const prozent = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 1 });
  const ROEMISCH = ['I', 'II', 'III'];
  const BETRAGSFELDER = ['versorgungsbezuege', 'bank', 'wertpapiere', 'immobilien', 'vermietet', 'familienheim',
    'sonstiges', 'hausrat', 'beweglich', 'schulden', 'kosten', 'vorerwerb', 'vorsteuer'];

  const auswahl = $('beziehung');
  for (const [schluessel, b] of Object.entries(BEZIEHUNGEN)) {
    auswahl.add(new Option(b.label, schluessel, false, schluessel === 'kind'));
  }

  const tarifBody = $('tarif').tBodies[0];
  TARIF.forEach(stufe => {
    const tr = tarifBody.insertRow();
    tr.insertCell().textContent = stufe.bis === Infinity ? 'darüber' : euro.format(stufe.bis);
    stufe.saetze.forEach(s => { tr.insertCell().textContent = s + ' %'; });
  });

  // Deutsche Schreibweise: Punkt als Tausendertrenner, Komma als Dezimalzeichen
  function leseBetrag(id) {
    const roh = $(id).value.replace(/\s|€/g, '').replace(/\./g, '').replace(',', '.');
    const wert = parseFloat(roh);
    return Number.isFinite(wert) && wert > 0 ? wert : 0;
  }

  function eingaben() {
    const e = {
      art: document.querySelector('input[name="art"]:checked').value,
      beziehung: auswahl.value,
      alterKind: parseInt($('alterKind').value, 10) || 0,
      quote: leseBetrag('quote'),
      wohnflaeche: parseFloat($('wohnflaeche').value) || 0,
      selbstgenutzt: $('selbstgenutzt').checked,
      pflege: $('pflege').checked
    };
    BETRAGSFELDER.forEach(id => { e[id] = leseBetrag(id); });
    return e;
  }

  function sichtbarkeit(e) {
    const erbschaft = e.art === 'erbschaft';
    const kindlich = e.beziehung === 'kind' || e.beziehung === 'enkel_verst';
    $('feld-quote').hidden = !erbschaft;
    $('feld-kosten').hidden = !erbschaft;
    $('feld-pflege').hidden = !erbschaft;
    $('feld-alter').hidden = !(erbschaft && kindlich);
    $('feld-versorgung').hidden = !(erbschaft && (kindlich || e.beziehung === 'ehegatte'));
    $('feld-wohnflaeche').hidden = !(erbschaft && kindlich);
    $('legende-vermoegen').textContent = erbschaft ? 'Nachlass (Verkehrswerte)' : 'Geschenktes Vermögen (Verkehrswerte)';

    let heim = '';
    if (e.beziehung === 'ehegatte') heim = 'Für Ehegatten ist das Familienheim vollständig steuerfrei.';
    else if (erbschaft && kindlich) heim = 'Befreiung nur bei unverzüglicher Selbstnutzung durch das Kind.';
    else heim = 'Für diesen Erwerber gibt es keine Befreiung für das Familienheim. Der Wert wird voll angesetzt.';
    $('familienheim-hinweis').textContent = heim;
  }

  function aktualisieren() {
    const e = eingaben();
    sichtbarkeit(e);
    const r = berechne(e);

    $('klasse-hinweis').textContent =
      `Steuerklasse ${ROEMISCH[r.stkl - 1]}, persönlicher Freibetrag ${euro.format(r.freibetrag)}` +
      (r.versorgung > 0 ? `, Versorgungsfreibetrag ${euro.format(r.versorgung)}` : '') + '.';

    $('steuer').textContent = euro.format(r.steuer);
    $('steuer-mobil').textContent = euro.format(r.steuer);
    $('k-stkl').textContent = ROEMISCH[r.stkl - 1];
    $('k-satz').textContent = r.stpflErwerb > 0 ? r.satz + ' %' : '–';
    $('k-effektiv').textContent = prozent.format(r.effektiv) + ' %';
    $('k-netto').textContent = euro.format(r.netto);

    const body = $('rechenweg').tBodies[0];
    body.replaceChildren();
    r.zeilen.forEach(z => {
      const tr = body.insertRow();
      if (z.summe) tr.className = 'summe';
      const text = tr.insertCell();
      text.textContent = z.text;
      if (z.ref) {
        const ref = document.createElement('span');
        ref.className = 'ref';
        ref.textContent = z.ref;
        text.append(ref);
      }
      tr.insertCell().textContent = (z.betrag < 0 ? '− ' : '') + zahl.format(Math.abs(z.betrag)) + ' €';
    });
    const tr = body.insertRow();
    tr.insertCell().textContent = 'Festzusetzende Steuer';
    tr.insertCell().textContent = zahl.format(r.steuer) + ' €';

    [...tarifBody.rows].forEach((row, i) => {
      [...row.cells].forEach((cell, j) => {
        cell.classList.toggle('aktiv', r.stpflErwerb > 0 && i === r.stufe && j === r.stkl);
      });
    });
  }

  BETRAGSFELDER.concat('quote').forEach(id => {
    $(id).addEventListener('blur', () => {
      const wert = leseBetrag(id);
      $(id).value = id === 'quote' ? prozent.format(Math.min(wert, 100)) : zahl.format(wert);
    });
  });

  $('formular').addEventListener('input', aktualisieren);
  $('formular').addEventListener('change', aktualisieren);
  $('formular').addEventListener('submit', ev => ev.preventDefault());
  aktualisieren();
})();
