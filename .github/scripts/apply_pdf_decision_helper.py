from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '<style id="decisionPdfPrintFix">'
if marker in s:
    print('Fix already present.')
    raise SystemExit(0)

addition = r'''

  <style id="decisionPdfPrintFix">
    @media print {
      @page { size:A4; margin:8mm; }
      #calculatorPrintSummary {
        width:194mm !important;
        max-width:194mm !important;
        margin:0 auto !important;
        font-size:7.9pt !important;
        line-height:1.16 !important;
      }
      .print-page {
        display:block !important;
        width:194mm !important;
        height:auto !important;
        min-height:0 !important;
        max-height:none !important;
        position:static !important;
        overflow:visible !important;
        break-inside:auto !important;
        page-break-inside:auto !important;
      }
      #printFundingPage {
        break-before:auto !important;
        page-break-before:auto !important;
        break-after:page !important;
        page-break-after:always !important;
      }
      #printHeatingPage {
        break-before:auto !important;
        page-break-before:auto !important;
        break-after:auto !important;
        page-break-after:auto !important;
      }
      #printFundingPage .print-title { font-size:19pt !important; margin:.7mm 0 .3mm !important; }
      #printFundingPage .print-subtitle { font-size:8pt !important; margin:0 0 1.5mm !important; }
      #printFundingPage .print-section-title { font-size:12.5pt !important; margin:0 0 1mm !important; padding-bottom:.7mm !important; }
      #printFundingPage .print-intro { margin:0 0 1.3mm !important; }
      #printFundingPage .print-block-title { font-size:8pt !important; margin:0 0 .6mm !important; }
      #printFundingPage .print-primary-grid { gap:1mm !important; margin-bottom:1.3mm !important; }
      #printFundingPage .print-primary-item { padding:1.6mm 2mm !important; }
      #printFundingPage .print-primary-item .print-value { font-size:12.5pt !important; margin-top:.3mm !important; }
      #printFundingPage .print-facts-grid { gap:1mm !important; margin-bottom:1.3mm !important; }
      #printFundingPage .print-fact { padding:1mm 1.4mm !important; min-height:8.5mm !important; }
      #printFundingPage .print-label { font-size:6.5pt !important; margin-bottom:.3mm !important; }
      #printFundingPage .print-value { font-size:9.5pt !important; }
      #printFundingPage .print-finance-compare { margin:0 0 1mm !important; border-radius:2mm !important; overflow:hidden !important; }
      #printFundingPage .print-finance-heading { padding:1.2mm 1.8mm !important; font-size:7.3pt !important; }
      #printFundingPage .decision-finance-grid { display:grid !important; grid-template-columns:1fr 1fr !important; }
      #printFundingPage .decision-finance-card { padding:1.4mm 2mm !important; background:#fff !important; }
      #printFundingPage .decision-finance-card + .decision-finance-card { border-left:1px solid #d8e1e4 !important; }
      #printFundingPage .decision-finance-card h4 { margin:0 0 .7mm !important; color:#071a2c !important; font-size:8.4pt !important; }
      #printFundingPage .decision-finance-row { display:flex !important; justify-content:space-between !important; gap:2mm !important; padding:.35mm 0 !important; border-top:1px solid #edf1f2 !important; }
      #printFundingPage .decision-finance-row span { color:#627080 !important; font-size:6.5pt !important; }
      #printFundingPage .decision-finance-row strong { color:#071a2c !important; font-size:7.6pt !important; text-align:right !important; }
      #printFundingPage .decision-finance-row.rate strong { color:#5ba646 !important; font-size:10.5pt !important; }
      #printFundingPage .print-finance-note { padding:.8mm 1.8mm !important; font-size:6.2pt !important; line-height:1.12 !important; }
      #printFundingPage .print-bonuses,
      #printFundingPage .print-requirements { padding:1mm 1.5mm !important; margin:0 0 .7mm !important; }
      #printFundingPage .print-bonuses h3,
      #printFundingPage .print-requirements h3 { font-size:7.2pt !important; margin:0 0 .25mm !important; }
      #printFundingPage .print-bonuses ul,
      #printFundingPage .print-requirements ul { margin:0 !important; padding-left:3.6mm !important; columns:2 !important; column-gap:4mm !important; }
      #printFundingPage .print-bonuses li,
      #printFundingPage .print-requirements li { margin:0 !important; font-size:6.1pt !important; line-height:1.10 !important; }
      .print-disclaimer {
        position:static !important;
        left:auto !important;
        right:auto !important;
        bottom:auto !important;
        margin-top:.5mm !important;
        padding:1mm 1.5mm !important;
        font-size:6.1pt !important;
        line-height:1.12 !important;
      }
      #printHeatingPage .print-disclaimer { margin-top:0 !important; }
    }
  </style>

  <script id="decisionPdfPrintScript">
    (()=>{
      const RATE = 0.0599;
      const previousBuild = buildCalculatorPrintSummary;
      buildCalculatorPrintSummary = function(){
        previousBuild();
        const price = Math.max(0, Number(document.getElementById('purchasePrice').value) || 0);
        const ownText = document.getElementById('ownShare').textContent || '0';
        const own = Math.max(0, Number(ownText.replace(/[^\d-]/g,'')) || 0);
        const years = Number(financeTerm) || 10;
        const ownMonthly = monthlyAnnuity(own, RATE, years);
        const fullMonthly = monthlyAnnuity(price, RATE, years);
        const compare = document.querySelector('#printFundingPage .print-finance-compare');
        if(!compare) return;
        compare.innerHTML = `
          <div class="print-finance-heading">Finanzierung im direkten Vergleich</div>
          <div class="decision-finance-grid">
            <div class="decision-finance-card">
              <h4>Variante A · Eigenanteil finanzieren</h4>
              <div class="decision-finance-row"><span>Finanzierungsbetrag</span><strong>${euro.format(own)}</strong></div>
              <div class="decision-finance-row"><span>Laufzeit</span><strong>${years} Jahre</strong></div>
              <div class="decision-finance-row"><span>Sollzins</span><strong>5,99 %</strong></div>
              <div class="decision-finance-row rate"><span>Monatsrate</span><strong>ca. ${Math.round(ownMonthly).toLocaleString('de-DE')} €</strong></div>
            </div>
            <div class="decision-finance-card">
              <h4>Variante B · Gesamtkosten finanzieren</h4>
              <div class="decision-finance-row"><span>Finanzierungsbetrag</span><strong>${euro.format(price)}</strong></div>
              <div class="decision-finance-row"><span>Laufzeit</span><strong>${years} Jahre</strong></div>
              <div class="decision-finance-row"><span>Sollzins</span><strong>5,99 %</strong></div>
              <div class="decision-finance-row rate"><span>Monatsrate</span><strong>ca. ${Math.round(fullMonthly).toLocaleString('de-DE')} €</strong></div>
            </div>
          </div>
          <p class="print-finance-note"><strong>Entscheidungshilfe:</strong> Variante A zeigt die Finanzierung nach Abzug der voraussichtlichen Förderung. Variante B zeigt die Finanzierung der gesamten Investitionskosten. Ob und wie eine spätere Förderung bei einer Finanzierung berücksichtigt wird, richtet sich nach dem jeweiligen Kreditvertrag. Unverbindliche Rechenbeispiele, keine Kreditangebote.</p>`;
      };
    })();
  </script>
'''

needle = '\n<!-- GALVANY V5.7 Preview'
if needle not in s:
    raise SystemExit('Insertion marker not found')
s = s.replace(needle, addition + '\n\n<!-- GALVANY V5.7 Preview', 1)
p.write_text(s, encoding='utf-8')
print('PDF decision helper patch applied.')
