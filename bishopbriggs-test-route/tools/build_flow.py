import json, html
ROOT = '/home/user/scotloand-trip/bishopbriggs-test-route/'
esc = lambda s: html.escape(s or '', quote=True)
PTS = json.load(open(ROOT + 'data/flow-points.json'))
PTS['A10']['back'] = [55.87690, -4.23230, 8]
SV = lambda p: f'https://www.google.com/maps/@?api=1&amp;map_action=pano&amp;viewpoint={p[0]},{p[1]}&amp;heading={p[2]}&amp;pitch=0&amp;fov=90'
G = {'left': '←', 'through': '↑', 'right': '→', 'slight_left': '↖', 'one': '↑', '?': '?'}
def chips(lanes, use):
    out = []
    for i, t in enumerate(lanes):
        g = ''.join(G.get(x, '?') for x in t.split(';'))
        cls = 'lc on' if i in use else 'lc'
        if t == '?': cls += ' q'
        out.append(f'<span class="{cls}">{g}</span>')
    return '<span class="chips" aria-hidden="true">' + ''.join(out) + '</span>'
POS = {0: 'LEFT', 1: 'RIGHT'}
def lane_word(lanes, use):
    n = len(lanes); i = use[0]
    if n == 1: return 'One lane: normal position'
    w = 'LEFT' if i == 0 else ('RIGHT' if i == n-1 else 'MIDDLE')
    return f'{w} lane (of {n})'
def R(kind, lanes, use, head, sig=None, leave=None, limit='40 mph', trap=None, mirrors=None, speed=None, look=None, signal=None, position=None):
    n = len(lanes); i = use[0]; moving_right = n > 1 and i > 0
    if mirrors is None:
        if kind == 'rbt':
            mirrors = 'Interior + left mirror' if sig == 'L' else ('Interior + right mirror' if (sig == 'R' or moving_right) else 'Interior mirror')
        elif moving_right: mirrors = 'Interior + right mirror before moving across (right blind spot if you change lane)'
        else: mirrors = 'Interior mirror, before you slow down'
    if signal is None:
        signal = {'L': '◀ Left, on approach', 'R': 'Right ▶, on approach'}.get(sig, 'None on approach' if kind == 'rbt' else 'None (straight on)')
    if position is None: position = lane_word(lanes, use)
    if speed is None:
        speed = {'rbt': 'Brake early: 2nd gear, about 10–15 mph, ready to stop at the give-way line',
                 'lights': f'Within {limit}, ready to stop. On amber, stop unless it is unsafe to do so',
                 'junction': f'Within {limit}, cover the brake'}.get(kind, f'Within {limit}')
    if look is None:
        look = {'rbt': 'Right, for traffic already on the roundabout. Go into a safe gap, or stop at the line',
                'lights': 'The lights, pedestrians crossing, and vehicles turning across you',
                'junction': 'The side road, for cars pulling out or turning in'}.get(kind, 'Ahead and in the mirrors')
    return dict(lanes=lanes, use=use, head=head, rows=[('Mirrors', mirrors), ('Signal', signal), ('Position', position), ('Speed', speed), ('Look', look)] + ([('Leave', leave)] if leave else []), trap=trap)
ONE = ['one']; Q = ['?']; Q2 = ['?', '?']
# (id, label, kind, card, [(direction label, cls, row, sv key)])
TRUNK = [
 ('S0', 'Test centre gate', 'T-junction', 'j01-gate-cole', [
   ('▶ OUT', 'out', R('turn', ONE, [0], 'Turn LEFT onto Crosshill Road', mirrors='Interior + left mirror (blind spots before moving off)', signal='◀ Left, before the give-way line', position='Left side of the exit road', speed='Creep to the line in 1st gear', look='Right, left, right again; go when clear', leave='Then at once: interior + left mirror, ◀ signal again for Cole Road roundabout, 57 m ahead'), 'out'),
   ('◀ BACK', 'back', R('turn', ONE, [0], 'Turn RIGHT into the test centre', mirrors='Interior + right mirror', signal='Right ▶, once you have left the roundabout', position='Just left of the centre line', speed='Slow, 2nd gear, ready to stop', look='Oncoming traffic and pedestrians at the entrance; turn when clear'), 'back')]),
 ('S1', 'Cole Road roundabout', 'Roundabout', 'j01-gate-cole', [
   ('▶ OUT', 'out', R('rbt', ONE, [0], '1st exit (it looks straight on)', sig='L', leave='Keep ◀ on; left mirror for cyclists as you leave'), 'out'),
   ('◀ BACK', 'back', R('rbt', ONE, [0], '2nd exit, past 12 o\'clock: treat as right', sig='R', position='One lane: keep towards the right, near the centre line', leave='Left mirror, ◀ signal once past Cole Road'), 'back')]),
 ('S2', 'Retail park lights', 'Lights', 'j02-retail-lights', [
   ('▶ OUT', 'out', R('lights', ['through;left'], [0], 'Straight on'), 'out'),
   ('◀ BACK', 'back', R('lights', ['through', 'right'], [0], 'Straight on', trap='Right lane is for the retail park only'), 'back')]),
 ('S3', 'Lowmoss Roundabout', 'Roundabout', 'j03-lowmoss', [
   ('▶ OUT', 'out', R('rbt', ['left', 'through;right'], [1], '2nd exit, ahead', trap='Left lane is LEFT ONLY', leave='Left mirror + left blind spot, ◀ signal once past the retail-park exit'), 'out'),
   ('◀ BACK', 'back', R('rbt', Q, [0], '2nd exit, just past 12 o\'clock: treat as ahead', trap='Lane arrows not mapped this way', leave='Left mirror, ◀ signal once past the Burger King exit'), 'back')]),
 ('S4', 'Cadder Roundabout (A803)', 'Roundabout · fork', 'j04-cadder', [
   ('▶ OUT to A', 'out', R('rbt', ['through', 'right'], [0], 'To A (south): 1st exit', sig='L', leave='Keep ◀ on; left mirror as you leave'), 'out'),
   ('▶ OUT to B', 'out', R('rbt', ['through', 'right'], [1], 'To B (north): 2nd exit', sig='R', leave='Left mirror + left blind spot, ◀ signal once past the A803 south exit'), 'out'),
   ('◀ BACK from A', 'back', R('rbt', ['left', 'right'], [1], 'Crosshill Road: 2nd exit', leave='Left mirror + left blind spot, ◀ signal once past the A803 north exit'), 'back_a'),
   ('◀ BACK from B', 'back', R('rbt', ['left', 'right'], [0], 'Crosshill Road: 1st exit', sig='L', leave='Keep ◀ on; left mirror as you leave'), 'back_b')]),
]
A = [
 ('A1', 'Side road by Shell Lowmoss', 'Junction', 'a1-cadder-road', [
   ('▶ OUT', 'out', R('junction', ['through', 'right'], [0], 'Straight on', trap='Right lane is for the side road only'), 'out'),
   ('◀ BACK', 'back', R('junction', ['through', 'right'], [0], 'Straight on', trap='Right lane turns towards Shell'), 'back')]),
 ('A2', 'Westerhill Road lights', 'Lights', 'a2-westerhill-lights', [
   ('▶ OUT', 'out', R('lights', ['left', 'through'], [1], 'Straight on', trap='Left lane is LEFT ONLY into Westerhill Road'), 'out'),
   ('◀ BACK', 'back', R('lights', ['through', 'right'], [0], 'Straight on', trap='Right lane is for Westerhill Road only'), 'back')]),
 ('A3', 'Meadowburn', 'Junction', 'a3-meadowburn', [
   ('▶ OUT', 'out', R('junction', ['through', 'right'], [0], 'Straight on', trap='Right lane is for Meadowburn only'), 'out'),
   ('◀ BACK', 'back', R('junction', ONE, [0], 'Straight on'), 'back')]),
 ('A4', 'Asda lights', 'Lights', 'a45-asda-hilton', [
   ('▶ OUT', 'out', R('lights', ['through;left', 'through', 'right'], [0], 'Straight on (middle lane also ahead)'), 'out'),
   ('◀ BACK', 'back', R('lights', ['left;through', 'through', 'right'], [0], 'Straight on (middle lane also ahead)', trap='Right lane turns into Asda'), 'back')]),
 ('A4b', 'Hilton Road lights', 'Lights', 'a45-asda-hilton', [
   ('▶ OUT', 'out', R('lights', ['through', 'through', 'right'], [0], 'Straight on', trap='Right lane is for Hilton Road only. 30 mph starts about 110 m after'), 'out'),
   ('◀ BACK', 'back', R('lights', ['left;through', 'through'], [0], 'Straight on', limit='30 mph', trap='Limit rises to 40 mph here'), 'back')]),
 ('A5', 'South Crosshill Road lights', 'Lights', 'a7-crosshill-lights', [
   ('▶ OUT', 'out', R('lights', ONE, [0], 'Straight on', limit='30 mph'), 'out'),
   ('◀ BACK', 'back', R('lights', Q2, [0], 'Straight on', limit='30 mph', trap='Arrows not mapped: read the road'), 'back')]),
 ('A5b', 'Springfield Road lights (Morrisons)', 'Lights', None, [
   ('▶ OUT', 'out', R('lights', Q2, [1], 'Straight on, setting up for the middle lane at Bishopbriggs Cross', limit='30 mph', trap='Arrows not mapped: read the road'), 'out'),
   ('◀ BACK', 'back', R('lights', ['through', 'through', 'right'], [0], 'Straight on', limit='30 mph', trap='Right lane is for Springfield Road only'), 'back')]),
 ('A6', 'Bishopbriggs Cross', 'Lights', 'a89-bishopbriggs-cross', [
   ('▶ OUT', 'out', R('lights', ['left', 'through;slight_left', 'right'], [1], 'Straight on (road bears slightly left)', limit='30 mph', trap='Left = Crowhill Road only, right = Kenmure Avenue'), 'out'),
   ('◀ BACK', 'back', R('lights', ['through', 'through', 'right'], [0], 'Straight on', limit='30 mph', trap='Right lane is for Crowhill Road only'), 'back')]),
 ('A7', 'Colston Road crossroads', 'Lights', 'a11-colston-road', [
   ('▶ OUT', 'out', R('lights', Q, [0], 'Straight on', limit='30 mph', position='Left lane', trap='Arrows not mapped: read the road'), 'out'),
   ('◀ BACK', 'back', R('lights', Q2, [0], 'Straight on', limit='30 mph', trap='Arrows not mapped: read the road'), 'back')]),
 ('A8', 'Springburn Road dual carriageway (by Shell)', 'Road change', None, [
   ('▶ OUT', 'out', R('road', ['through', 'through'], [0], 'Dual carriageway starts', speed='Limit 40 mph; keep a 2-second gap', look='Shell on your right; keep left unless overtaking'), 'out'),
   ('◀ BACK', 'back', R('road', ['through'], [0], 'Lanes reduce to one near the railway bridge (mapped)', mirrors='Interior + left mirror before you merge', signal='◀ Left only if you have to move across', position='LEFT lane, early', speed='Within 40 mph; merge in turn', look='Traffic beside you in the right lane'), 'back')]),
 ('A9', 'Atlas Road / Keppochhill Road lights', 'Lights', None, [
   ('▶ OUT', 'out', R('lights', Q2, [0], 'Straight on', trap='Arrows not mapped: check Street View'), 'out'),
   ('◀ BACK', 'back', R('lights', Q2, [0], 'Straight on', trap='Arrows not mapped: check Street View'), 'back')]),
 ('A10', 'Petershill Road lights (end of A)', 'Lights · end', None, [
   ('▶ OUT', 'out', R('lights', Q2, [0], 'Last lights in this guide (≈3.9 miles)', trap='Petershill Road is on your left'), 'out'),
   ('◀ BACK', 'back', R('lights', Q2, [0], 'Return starts here, heading north'), 'back')]),
]
B = [
 ('B0', 'Kirkintilloch Road north', 'Road change', None, [
   ('▶ OUT', 'out', R('road', ONE, [0], 'Limit rises to 60 mph', speed='Build up to 60 smoothly, only as conditions allow', look='Far ahead: bends, cyclists, slow vehicles'), None),
   ('◀ BACK', 'back', R('road', ONE, [0], 'Limit drops to 40 mph before Cadder', speed='Be at 40 by the signs, then start the roundabout routine', look='The queue for Cadder Roundabout'), None)]),
 ('B1', 'Torrance Roundabout', 'Roundabout', 'b1-torrance', [
   ('▶ OUT', 'out', R('rbt', ['left', 'through;right'], [1], '2nd exit, ahead to Kirkintilloch', speed='From 60 mph: brake early, 2nd gear, about 10–15 mph', trap='Left lane is LEFT ONLY', leave='Left mirror + left blind spot, ◀ signal once past Torrance Road'), 'out'),
   ('◀ BACK', 'back', R('rbt', ['left', 'through;right'], [1], '2nd exit, ahead to Cadder', speed='From 60 mph: brake early, 2nd gear, about 10–15 mph', trap='Left lane is Cole Road only', leave='Left mirror + left blind spot, ◀ signal once past Cole Road'), 'back')]),
 ('B1b', 'Glasgow Road, Kirkintilloch', 'Road change', None, [
   ('▶ OUT', 'out', R('road', ONE, [0], 'Limit drops from 60 to 30 mph', speed='Be at 30 by the signs', look='Pedestrians and parked cars from here on'), None),
   ('◀ BACK', 'back', R('road', ONE, [0], 'Limit rises from 30 to 60 mph', speed='Build up smoothly after the signs', look='Far ahead on the open road'), None)]),
 ('B2', 'Peel Park Roundabout', 'Roundabout', 'b2-peel-park', [
   ('▶ OUT', 'out', R('rbt', ONE, [0], '1st exit (it looks straight on)', sig='L', leave='Keep ◀ on; left mirror as you leave'), 'out'),
   ('◀ BACK', 'back', R('rbt', ONE, [0], '2nd exit, just past 12 o\'clock: treat as ahead', leave='Left mirror, ◀ signal once past West High Street'), 'back')]),
 ('B3', 'New Lairdsland Road lights', 'Lights', 'b3-new-lairdsland', [
   ('▶ OUT', 'out', R('lights', ['through', 'right'], [0], 'Straight on', limit='30 mph', trap='Right lane turns into the A806'), 'out'),
   ('◀ BACK', 'back', R('lights', ['left', 'through'], [1], 'Straight on', limit='30 mph', trap='Left lane is LEFT ONLY into the A806'), 'back')]),
 ('B4', 'Milton Road lights', 'Lights', 'b4-milton-road', [
   ('▶ OUT', 'out', R('lights', ['left;through', 'right'], [0], 'Straight on', limit='30 mph', trap='Right lane is for Ledgate only'), 'out'),
   ('◀ BACK', 'back', R('lights', ['left;through', 'right'], [0], 'Straight on', limit='30 mph', trap='Right lane is for Milton Road only'), 'back')]),
 ('B5', 'Eastside Roundabout', 'Roundabout', None, [
   ('▶ OUT', 'out', R('rbt', ONE, [0], '2nd exit, ahead on Kilsyth Road', leave='Left mirror, ◀ signal once past Kelvinvale'), 'out'),
   ('◀ BACK', 'back', R('rbt', ONE, [0], '2nd exit, just past 12 o\'clock: treat as ahead', leave='Left mirror, ◀ signal once past Eastside'), 'back')]),
 ('B6', 'Kilsyth Road, 40 mph sign (end of B)', 'Road change · end', None, [
   ('▶ OUT', 'out', R('road', ONE, [0], 'Limit rises to 40 mph (≈4.1 miles, end of guide)', speed='Up to 40 smoothly'), 'out'),
   ('◀ BACK', 'back', R('road', ONE, [0], 'Return starts here: 30 mph into Kirkintilloch', speed='Be at 30 by the signs'), 'back')]),
]
def km(sid):
    p = PTS.get(sid)
    return p['km'] if p else {'B0': 0.9, 'B1b': 3.8}.get(sid)
def dirrow(lab, cls, r, key, p):
    lk = f'<a class="sv" href="{SV(p[key])}" target="_blank" rel="noopener">Street View ↗</a>' if key and p.get(key) else ''
    trap = f'<p class="dtrap">{esc(r["trap"])}</p>' if r.get('trap') else ''
    rows = ''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k, v in r['rows'])
    return f'<div class="dir {cls}"><div class="dh"><span class="dl">{esc(lab)}</span>{chips(r["lanes"], r["use"])}<b>{esc(r["head"])}</b></div>{trap}<dl class="msm">{rows}</dl>{lk}</div>'
def stop(s, branch):
    sid, label, kind, card, dirs = s
    p = PTS.get(sid, {}); k = km(sid)
    kms = f'<span class="km">{k:.1f} km</span>' if k is not None else ''
    det = f'<a class="det" href="#{card}">Drawing ↓</a>' if card else ''
    rows = ''.join(dirrow(lab, cls, r, key, p) for lab, cls, r, key in dirs)
    sidt = sid.replace('S', '') if branch == 'S' else sid
    return f'<li class="stop {"minor" if kind.startswith("Road change") else ""}" id="f-{sid}"><div class="st-head"><span class="sid">{esc(sidt)}</span><div><b>{esc(label)}</b><span class="kind">{esc(kind)}</span></div>{kms}{det}</div>{rows}</li>'
def block(title, cls, items, branch, note):
    return f'<div class="blk {cls}"><h3>{title}</h3><p class="bn">{note}</p><ol class="stops">' + '\n'.join(stop(s, branch) for s in items) + '</ol></div>'
html_out = f'''<section class="flow" id="flow" aria-labelledby="flow-h">
  <div class="leghead"><h2 id="flow-h">Route flow: out and back</h2>
  <p class="muted">Every junction on both branches, in order. Each direction gives your lane (blue chip), then the full routine: <b>Mirrors, Signal, Position, Speed, Look</b>, and for roundabouts how to <b>Leave</b>. The Street View link faces the way you will be driving. Choose "Coming back" to list the stops in return order.</p></div>
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
