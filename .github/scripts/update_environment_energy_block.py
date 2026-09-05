from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''        <div class="dimension-panel">
          <h3>Aus Strom wird Wärme.</h3>
          <div class="energy-flow" aria-label="Eine Kilowattstunde Strom ergibt ungefähr drei bis fünf Kilowattstunden Wärme">
            <div class="energy-value">1 kWh Strom</div>
            <div class="energy-arrow" aria-hidden="true"></div>
            <div class="energy-value heat">ca. 3–5 kWh Wärme</div>
          </div>
          <p class="energy-copy">Eine Wärmepumpe erzeugt die Wärme nicht ausschließlich aus Strom. Sie nutzt zusätzlich Energie aus der Umgebung.</p>
        </div>'''

new = '''        <div class="dimension-panel">
          <h3>Wärme aus der Umwelt.</h3>
          <div class="energy-flow" aria-label="Aus ungefähr zwei bis vier Kilowattstunden Umweltenergie und einer Kilowattstunde Strom entstehen ungefähr drei bis fünf Kilowattstunden nutzbare Wärme">
            <div class="energy-value heat">ca. 2–4 kWh Umweltenergie</div>
            <div class="energy-value" style="font-size:clamp(1.8rem,4vw,3.5rem);letter-spacing:-.04em">+ 1 kWh Strom</div>
            <div class="energy-arrow" aria-hidden="true"></div>
            <div class="energy-value heat">ca. 3–5 kWh Wärme</div>
          </div>
          <p class="energy-copy">Die Wärmepumpe nutzt kostenlose Energie aus der Umgebungsluft. Strom wird benötigt, um diese Umweltwärme auf das erforderliche Temperaturniveau für Heizung und Warmwasser anzuheben.</p>
        </div>'''

if old not in s:
    if '<h3>Wärme aus der Umwelt.</h3>' in s:
        print('Environment energy block already updated.')
        raise SystemExit(0)
    raise SystemExit('Expected energy block not found; no changes made.')

p.write_text(s.replace(old, new, 1), encoding='utf-8')
print('Environment energy block updated.')
