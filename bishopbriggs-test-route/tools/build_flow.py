import json, html
ROOT = '/home/user/scotloand-trip/bishopbriggs-test-route/'
esc = lambda s: html.escape(s or '', quote=True)
PTS = json.load(open(ROOT + 'data/flow-points.json'))
PTS['A10']['back'] = [55.87690, -4.23230, 8]
SV = lambda p: f'https://www.google.com/maps/@?api=1&amp;map_action=pano&amp;viewpoint={p[0]},{p[1]}&amp;heading={p[2]}&amp;pitch=0&amp;fov=90'
G = {'left': '←', 'through': '↑', 'right': '→', 'slight_left': '↖', 'one': '↑', '?': '?'}
def chips(lanes, use):
    if not lanes: return ''
    out = []
    for i, t in enumerate(lanes):
        g = ''.join(G.get(x, '?') for x in t.split(';'))
        cls = 'lc on' if i in use else 'lc'
        if t == 'one': cls += ' one'
        if t == '?': cls += ' q'
        out.append(f'<span class="{cls}">{g}</span>')
    return '<span class="chips" aria-hidden="true">' + ''.join(out) + '</span>'
def d(lanes, use, text): return dict(lanes=lanes, use=use, text=text)
# id: (label, kind, card anchor, out, back[, extra back rows])
TRUNK = [
 ('S0', 'Test centre gate', 'T-junction', 'j01-gate-cole',
  d(['one'], [0], 'Turn LEFT out of the gate. ◀ Signal left. Look right, then left.'),
  d(['one'], [0], 'Turn RIGHT into the test centre 57 m after the roundabout. Signal right ▶ once you leave the roundabout, move towards the centre line, wait for a gap.')),
 ('S1', 'Cole Road roundabout', 'Roundabout', 'j01-gate-cole',
  d(['one'], [0], '1st exit (it looks straight on). ◀ Signal left on approach, keep left.'),
  d(['one'], [0], '2nd exit, past 12 o\'clock, so treat it as right: signal right ▶ on approach, keep right, ◀ signal left once past Cole Road.')),
 ('S2', 'Retail park lights', 'Lights', 'j02-retail-lights',
  d(['through;left'], [0], 'One lane. Straight on, no signal. Go on green.'),
  d(['through', 'right'], [0], 'LEFT lane for straight on. The right lane is only for the retail park. No signal.')),
 ('S3', 'Lowmoss Roundabout', 'Roundabout', 'j03-lowmoss',
  d(['left', 'through;right'], [1], 'RIGHT lane (left lane is left only). No signal on approach. 2nd exit: ◀ signal left once past the retail-park exit.'),
  d(['?'], [0], '2nd exit, just past 12 o\'clock: treat it as straight on. No signal on approach, ◀ signal left once past the Burger King exit. Lane arrows not mapped this way.')),
 ('S4', 'Cadder Roundabout (A803)', 'Roundabout · fork', 'j04-cadder',
  d(['through', 'right'], [0, 1], 'To A (south): LEFT lane, ◀ signal left, 1st exit. To B (north): RIGHT lane, signal right ▶, keep right, ◀ signal left after the A803 south exit.'),
  None,
  [('◀ BACK from A', d(['left', 'right'], [1], 'RIGHT lane (marked). Crosshill Road is the 2nd exit: no signal on approach, ◀ signal left once past the A803 north exit.'), 'back_a'),
   ('◀ BACK from B', d(['left', 'right'], [0], 'LEFT lane. ◀ Signal left on approach. 1st exit onto Crosshill Road.'), 'back_b')]),
]
A = [
 ('A1', 'Side road by Shell Lowmoss', 'Junction', 'a1-cadder-road',
  d(['through', 'right'], [0], 'LEFT lane. The right lane is for the side road only. No signal.'),
  d(['through', 'right'], [0], 'LEFT lane. The right lane turns right towards Shell. No signal.')),
 ('A2', 'Westerhill Road lights', 'Lights', 'a2-westerhill-lights',
  d(['left', 'through'], [1], 'RIGHT lane: the left lane is LEFT ONLY into Westerhill Road. No signal.'),
  d(['through', 'right'], [0], 'LEFT lane. The right lane is for Westerhill Road only. No signal.')),
 ('A3', 'Meadowburn', 'Junction', 'a3-meadowburn',
  d(['through', 'right'], [0], 'LEFT lane. The right lane is for Meadowburn only. No signal.'),
  d(['one'], [0], 'One lane. Straight on, no signal. Watch for cars turning into Meadowburn.')),
 ('A4', 'Asda lights', 'Lights', 'a45-asda-hilton',
  d(['through;left', 'through', 'right'], [0], 'LEFT lane (middle lane also goes ahead). The right lane turns right. No signal.'),
  d(['left;through', 'through', 'right'], [0], 'LEFT lane (middle also ahead). The right lane turns right into Asda. No signal.')),
 ('A4b', 'Hilton Road lights', 'Lights', 'a45-asda-hilton',
  d(['through', 'through', 'right'], [0], 'Stay LEFT. The right lane is for Hilton Road only. 30 mph starts about 110 m after.'),
  d(['left;through', 'through'], [0], 'Either lane goes ahead: keep LEFT. Left lane also turns into Hilton Road. Limit back up to 40 mph.')),
 ('A5', 'South Crosshill Road lights', 'Lights', 'a7-crosshill-lights',
  d(['one'], [0], 'One lane, straight on, no signal. 30 mph.'),
  d(['?', '?'], [0], 'Two lanes, arrows not mapped: keep LEFT for straight on. No signal.')),
 ('A5b', 'Springfield Road lights (Morrisons)', 'Lights', None,
  d(['?', '?'], [1], 'Two lanes, arrows not mapped. Take the right-hand one, ready for the middle lane at Bishopbriggs Cross.'),
  d(['through', 'through', 'right'], [0], 'LEFT or middle lane for straight on. The right lane is for Springfield Road only.')),
 ('A6', 'Bishopbriggs Cross', 'Lights', 'a89-bishopbriggs-cross',
  d(['left', 'through;slight_left', 'right'], [1], 'MIDDLE lane. Left = Crowhill Road only, right = Kenmure Avenue. No signal.'),
  d(['through', 'through', 'right'], [0], 'LEFT (or middle) lane. The right lane is for Crowhill Road only. No signal.')),
 ('A7', 'Colston Road crossroads', 'Lights', 'a11-colston-road',
  d(['?'], [0], 'Straight on, left lane. Arrows not mapped: read the road on the day.'),
  d(['?', '?'], [0], 'Two lanes, arrows not mapped: keep LEFT for straight on. No signal.')),
 ('A8', 'Springburn Road dual carriageway (by Shell)', 'Road change', None,
  d(['through', 'through'], [0], 'Dual carriageway starts, 40 mph. Two lanes: keep LEFT unless overtaking. Shell is on your right.'),
  d(['through'], [0], 'Northbound is mapped as narrowing to one lane near the railway bridge: be in the left lane early and merge in turn. Dual carriageway ends by Shell.')),
 ('A9', 'Atlas Road / Keppochhill Road lights', 'Lights', None,
  d(['?', '?'], [0], 'Lights on the dual carriageway. Arrows not mapped: use the left lane for ahead, check Street View.'),
  d(['?', '?'], [0], 'Lights. Arrows not mapped: left lane for ahead, check Street View.')),
 ('A10', 'Petershill Road lights (end of A)', 'Lights · end', None,
  d(['?', '?'], [0], 'Last set of lights in this guide, about 3.9 miles from the centre. Petershill Road is on your left.'),
  d(['?', '?'], [0], 'Return starts here, heading north on Springburn Road. Left lane, 40 mph.')),
]
B = [
 ('B0', 'Kirkintilloch Road north', 'Road change', None,
  d(['one'], [0], 'Just after Cadder the limit rises to 60 mph (national speed limit). Build up speed smoothly.'),
  d(['one'], [0], 'Limit drops to 40 mph just before Cadder Roundabout.')),
 ('B1', 'Torrance Roundabout', 'Roundabout', 'b1-torrance',
  d(['left', 'through;right'], [1], 'RIGHT lane (left lane is left only). No signal on approach. 2nd exit: ◀ signal left once past Torrance Road.'),
  d(['left', 'through;right'], [1], 'RIGHT lane (left lane is Cole Road only). No signal on approach. 2nd exit to Cadder: ◀ signal left once past Cole Road.')),
 ('B1b', 'Glasgow Road, Kirkintilloch', 'Road change', None,
  d(['one'], [0], '2 km of 60 mph road over the Forth and Clyde Canal, then the limit drops to 30 mph where it becomes Glasgow Road.'),
  d(['one'], [0], 'Leaving Kirkintilloch the limit rises from 30 to 60 mph.')),
 ('B2', 'Peel Park Roundabout', 'Roundabout', 'b2-peel-park',
  d(['one'], [0], '1st exit (looks straight on). ◀ Signal left on approach, keep left.'),
  d(['one'], [0], '2nd exit, just past 12 o\'clock: treat it as straight on. No signal on approach, ◀ signal left once past West High Street.')),
 ('B3', 'New Lairdsland Road lights', 'Lights', 'b3-new-lairdsland',
  d(['through', 'right'], [0], 'LEFT lane. The right lane turns right into the A806. No signal.'),
  d(['left', 'through'], [1], 'RIGHT lane: the left lane is LEFT ONLY into the A806. No signal.')),
 ('B4', 'Milton Road lights', 'Lights', 'b4-milton-road',
  d(['left;through', 'right'], [0], 'LEFT lane (also for Milton Road). The right lane is for Ledgate only. No signal.'),
  d(['left;through', 'right'], [0], 'LEFT lane (also for Ledgate). The right lane is for Milton Road only. No signal.')),
 ('B5', 'Eastside Roundabout', 'Roundabout', None,
  d(['one'], [0], 'One lane, no markings. 2nd exit, Kilsyth Road: no signal on approach, ◀ signal left once past Kelvinvale.'),
  d(['one'], [0], '2nd exit, just past 12 o\'clock: treat it as straight on. No signal on approach, ◀ signal left once past Eastside.')),
 ('B6', 'Kilsyth Road, 40 mph sign (end of B)', 'Road change · end', None,
  d(['one'], [0], 'Leaving Kirkintilloch the limit rises to 40 mph. End of this guide, about 4.1 miles from the centre.'),
  d(['one'], [0], 'Return starts here: 30 mph into Kirkintilloch.')),
]
FIX = {'B0': ('A', None), 'B1b': None}
def km(sid):
    p = PTS.get(sid)
    if p: return p['km']
    return {'B0': 0.9, 'B1b': 3.8}.get(sid)
def stop(s, branch):
    sid, label, kind, card, o, b = s[:6]; extra = s[6] if len(s) > 6 else []
    p = PTS.get(sid, {})
    k = km(sid); kms = f'<span class="km">{k:.1f} km</span>' if k is not None else ''
    det = f'<a class="det" href="#{card}">Drawing ↓</a>' if card else ''
    rows = []
    if o:
        lk = f'<a class="sv" href="{SV(p["out"])}" target="_blank" rel="noopener">Street View ↗</a>' if p.get('out') else ''
        rows.append(f'<div class="dir out"><span class="dl">▶ OUT</span>{chips(o["lanes"], o["use"])}<p>{esc(o["text"])}</p>{lk}</div>')
    if b:
        lk = f'<a class="sv" href="{SV(p["back"])}" target="_blank" rel="noopener">Street View ↗</a>' if p.get('back') else ''
        rows.append(f'<div class="dir back"><span class="dl">◀ BACK</span>{chips(b["lanes"], b["use"])}<p>{esc(b["text"])}</p>{lk}</div>')
    for lab, dd, key in extra:
        lk = f'<a class="sv" href="{SV(p[key])}" target="_blank" rel="noopener">Street View ↗</a>' if p.get(key) else ''
        rows.append(f'<div class="dir back"><span class="dl">{esc(lab)}</span>{chips(dd["lanes"], dd["use"])}<p>{esc(dd["text"])}</p>{lk}</div>')
    return f'''<li class="stop {'minor' if kind.startswith('Road change') else ''}" id="f-{sid}"><div class="st-head"><span class="sid">{esc(sid.replace('S', '') if branch == 'S' else sid)}</span><div><b>{esc(label)}</b><span class="kind">{esc(kind)}</span></div>{kms}{det}</div>{''.join(rows)}</li>'''
def block(title, cls, items, branch, note):
    return f'<div class="blk {cls}"><h3>{title}</h3><p class="bn">{note}</p><ol class="stops">' + '\n'.join(stop(s, branch) for s in items) + '</ol></div>'
html_out = f'''<section class="flow" id="flow" aria-labelledby="flow-h">
  <div class="leghead"><h2 id="flow-h">Route flow: out and back</h2>
  <p class="muted">Every junction on both branches, in order, with the lane and signal for each direction and a Street View link facing the way you will be driving. Blue lane chip = your lane. Choose "Coming back" to list the stops in return order.</p></div>
  <div class="modes" role="group" aria-label="Direction">
    <button type="button" data-mode="both" aria-pressed="true">Both ways</button>
    <button type="button" data-mode="out" aria-pressed="false">▶ Going out</button>
    <button type="button" data-mode="back" aria-pressed="false">◀ Coming back</button>
  </div>
  <div class="flowbody" id="flowbody">
    {block('Start: test centre ⇄ Cadder Roundabout', 'trunk', TRUNK, 'S', 'Crosshill Road, B819, 40 mph, 0.85 km.')}
    <div class="branches">
      {block('A · Asda side: A803 south', 'a', A, 'A', 'Bishopbriggs to Springburn, 6.2 km (3.9 miles) from the centre at the far end.')}
      {block('B · Torrance and Kirkintilloch side: A803 north', 'b', B, 'B', 'Torrance and Kirkintilloch, 6.6 km (4.1 miles) from the centre at the far end.')}
    </div>
  </div>
</section>'''
open(ROOT + 'data/flow.html', 'w').write(html_out)
print('flow', len(html_out)//1024, 'KB')
