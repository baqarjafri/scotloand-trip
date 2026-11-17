import json, html, math
ROOT = '/home/user/scotloand-trip/bishopbriggs-test-route/'
esc = lambda s: html.escape(s or '', quote=True)
SV = lambda lat, lon, h: f'https://www.google.com/maps/@?api=1&amp;map_action=pano&amp;viewpoint={lat},{lon}&amp;heading={h}&amp;pitch=0&amp;fov=90'
WORD = {'left': 'LEFT', 'through': 'AHEAD', 'right': 'RIGHT', 'slight_left': 'AHEAD', 'slight_right': 'AHEAD', '?': '?'}

def lane_view(lanes, kind, title, single_note=None):
    """Driver's-eye view of the approach: perspective lanes with painted arrows."""
    turns = lanes['turns'] if lanes else [single_note or 'one']
    n = len(turns); use = set(lanes['use']) if lanes else {0}; tags = (lanes or {}).get('tags') or {}
    VW, VH, top, bot = 400, 250, 46, 236
    wb, wt = 372, 118
    def X(u, v): return VW/2 + (u-0.5)*(wb-(wb-wt)*v)
    def Y(v): return bot - v*(bot-top)
    def P(u, v): return f'{X(u, v):.1f},{Y(v):.1f}'
    o = [f'<svg viewBox="0 0 {VW} {VH}" class="lane" role="img" aria-label="{esc(title)}">',
         f'<rect width="{VW}" height="{VH}" class="l-sky"/>',
         f'<polygon points="{P(0,0)} {P(1,0)} {P(1,1)} {P(0,1)}" class="l-road"/>']
    for i in range(n):
        if i in use:
            cls = 'l-on-b' if tags.get(str(i), tags.get(i)) == 'B' else 'l-on'
            o.append(f'<polygon points="{P(i/n,0)} {P((i+1)/n,0)} {P((i+1)/n,1)} {P(i/n,1)}" class="{cls}"/>')
    # markings
    o.append(f'<polyline points="{P(0.015,0)} {P(0.015,1)}" class="l-edge"/><polyline points="{P(0.985,0)} {P(0.985,1)}" class="l-edge"/>')
    for i in range(1, n):
        segs = [(k/9, k/9+0.06) for k in range(9)]
        for a, b in segs: o.append(f'<polyline points="{P(i/n,a)} {P(i/n,b)}" class="l-dash"/>')
    if kind == 'rbt':
        for vv in (0.955, 0.985):
            for k in range(14): o.append(f'<polyline points="{P(k/14+0.01,vv)} {P(k/14+0.05,vv)}" class="l-gw"/>')
    elif kind == 'lights':
        o.append(f'<polyline points="{P(0.01,0.97)} {P(0.99,0.97)}" class="l-stop"/>')
    # arrows
    for i, t in enumerate(turns):
        parts = t.split(';') if isinstance(t, str) else []
        cu = (i+0.5)/n; lw = 1/n
        def L(du, v): return (cu + du*lw, v)
        if not parts or parts == ['one'] or parts == ['?']:
            if parts == ['?']:
                x, y = X(cu, 0.45), Y(0.45); o.append(f'<text x="{x:.1f}" y="{y:.1f}" class="l-q" text-anchor="middle">?</text>')
            continue
        stem_top = 0.62 if ('through' in parts or 'slight_left' in parts) else 0.48
        o.append(f'<polyline points="{P(*L(0,0.18))} {P(*L(0,stem_top))}" class="l-arrow"/>')
        if 'through' in parts or 'slight_left' in parts or 'slight_right' in parts:
            o.append(f'<polygon points="{P(*L(0,0.80))} {P(*L(-0.17,0.60))} {P(*L(0.17,0.60))}" class="l-head"/>')
        for side, sg in (('left', -1), ('right', 1)):
            if side in parts:
                pts = [L(0, 0.40)] + [L(sg*0.30*math.sin(math.radians(a)), 0.40+0.16*(1-math.cos(math.radians(a)))) for a in range(15, 91, 15)]
                o.append(f'<polyline points="{" ".join(P(*q) for q in pts)}" class="l-arrow"/>')
                tip = L(sg*0.46, 0.56); b1 = L(sg*0.28, 0.66); b2 = L(sg*0.28, 0.46)
                o.append(f'<polygon points="{P(*tip)} {P(*b1)} {P(*b2)}" class="l-head"/>')
    # lane words at the bottom
    for i, t in enumerate(turns):
        parts = t.split(';') if isinstance(t, str) else []
        word = ' + '.join(dict.fromkeys(WORD.get(p, p.upper()) for p in parts)) if parts and parts != ['one'] else ('ONE LANE' if parts == ['one'] else '')
        if parts == ['?']: word = 'NOT MAPPED'
        if parts and len(parts) == 1 and parts[0] in ('left', 'right') and n > 1: word += ' ONLY'
        x = X((i+0.5)/n, 0.035); fs = 15 if n >= 3 else 17
        o.append(f'<text x="{x:.1f}" y="{bot-8:.1f}" text-anchor="middle" font-size="{fs}" class="l-word">{esc(word)}</text>')
    # your-lane tags above the road
    for i in sorted(use):
        tag = tags.get(str(i), tags.get(i)) or 'YOU'
        x = X((i+0.5)/n, 1.0); w = 18 + 11*len(tag)
        cls = 'l-tag-b' if tag == 'B' else 'l-tag'
        o.append(f'<rect x="{x-w/2:.1f}" y="10" width="{w}" height="26" rx="13" class="{cls}"/><text x="{x:.1f}" y="29" text-anchor="middle" class="l-tagt">{esc(tag)}</text>')
        o.append(f'<polyline points="{x:.1f},36 {x:.1f},{top-2}" class="l-tick {cls}"/>')
    if kind == 'lights':
        lx = X(0.0, 1.0) - 20
        o.append(f'<g><rect x="{lx-9:.1f}" y="6" width="18" height="40" rx="4" fill="#141414" stroke="#ffffff" stroke-width="1.5"/><circle cx="{lx:.1f}" cy="15" r="4.5" fill="#e6281e"/><circle cx="{lx:.1f}" cy="26" r="4.5" fill="#faaf00"/><circle cx="{lx:.1f}" cy="37" r="4.5" fill="#28be46"/></g>')
    if kind == 'rbt':
        o.append(f'<text x="{VW-10}" y="28" text-anchor="end" class="l-gwt">GIVE WAY ⟲</text>')
    o.append('</svg>')
    return '\n'.join(o)

CARDS = {
 'start': [
  ('j01-gate-cole', 'rbt', '0 → 57 m', (55.924483, -4.199844, 261)),
  ('j02-retail-lights', 'lights', '≈330 m', (55.923455, -4.203695, 238)),
  ('j03-lowmoss', 'rbt', '≈630 m', (55.922302, -4.207978, 215)),
  ('j04-cadder', 'rbt', '≈850 m', (55.921281, -4.209868, 235))],
 'a': [
  ('a1-cadder-road', 'priority', '70 m', (55.920805, -4.211227, 208)),
  ('a2-westerhill-lights', 'lights', '310 m', (55.918923, -4.213124, 208)),
  ('a3-meadowburn', 'priority', '610 m', (55.916574, -4.215451, 209)),
  ('a45-asda-hilton', 'lights', '0.9–1.0 km', (55.914499, -4.217505, 209)),
  'Speed limit drops to <b>30 mph</b> about 110 m after Hilton Road. Side roads at Wester Cleddens join with no lights and no lane choice: keep straight on and watch for cars pulling out.|1.1–1.8 km',
  ('a7-crosshill-lights', 'lights', '1.8 km', (55.907041, -4.224121, 184)),
  'Springfield Road (Morrisons) lights on your left, by the Triangle shopping centre. Straight on. Lane arrows are not mapped here.|≈1.95 km',
  ('a89-bishopbriggs-cross', 'lights', '2.1 km', (55.904651, -4.224603, 205)),
  'Over the railway bridge at Bishopbriggs station and through Auchinairn. Mostly one lane each way, 30 mph.|2.1–3.1 km',
  ('a11-colston-road', 'lights', '3.1 km', (55.896696, -4.231501, 180))],
 'b': [
  'Shortly after Cadder the limit rises to <b>60 mph</b> (national speed limit, single carriageway). Build up speed smoothly and only as conditions allow.|0–0.9 km',
  ('b1-torrance', 'rbt', '0.9 km', (55.927768, -4.204240, 25)),
  'About 2 km of 60 mph road across open country and over the Forth and Clyde Canal. At about 2.9 km it becomes Glasgow Road and the limit drops to <b>30 mph</b>: be at 30 by the signs.|0.9–3.9 km',
  ('b2-peel-park', 'rbt', '3.9 km', (55.940180, -4.164240, 45)),
  ('b3-new-lairdsland', 'lights', '4.2 km', (55.942650, -4.160067, 49)),
  ('b4-milton-road', 'lights', '4.5 km', (55.943044, -4.154919, 96))]}
LANECAP = {'a45-asda-hilton': 'Lanes at the first lights (Asda). At Hilton Road, 110 m on, they are ahead | ahead | right only: stay in the left lane.',
           'j04-cadder': 'Two lanes open up just before the give-way line. A = left lane, B = right lane.'}
SINGLE = {'j01-gate-cole': 'one', 'a7-crosshill-lights': 'one', 'b2-peel-park': 'one', 'a11-colston-road': '?'}

def card(name, kind, dist, sv):
    d = json.load(open(ROOT + 'diag/' + name + '.json')); h = d['head']
    lanes = d['lanes']
    if name in SINGLE: lanes = None
    lv = lane_view(lanes, kind, 'Lanes on the approach to ' + h['title'].title(), SINGLE.get(name))
    route = esc(h['route'])
    for k in ('RIGHT lane', 'LEFT lane', 'MIDDLE lane', 'RIGHT', 'LEFT ONLY'):
        pass
    opts = []
    for r in d['legend']:
        cls = 'opt primary' if r['primary'] else 'opt'
        opts.append(f'<li class="{cls}"><i class="sw{" dash" if r["dash"] else ""}" style="--sw:{r["color"]}" aria-hidden="true"></i><div><b>{esc(r["told"])}</b><span>{esc(r["line2"])}</span></div></li>')
    note = f'<p class="trap">{esc(d["note"])}</p>' if d.get('note') else ''
    lane_cap = LANECAP.get(name) or ('What you see on the approach: the lanes and their painted arrows.' if lanes else ('One lane on the approach: keep to your normal position.' if SINGLE.get(name) == 'one' else 'Lane arrows are not mapped here: read the road markings on the day.'))
    mph = f'<span class="mph" title="Speed limit {h["mph"]} mph">{h["mph"]}</span>' if h.get('mph') else ''
    return f'''<article class="jc" id="{name}">
  <div class="jh"><span class="jn">{esc(h["num"])}</span><div><h3>{esc(h["title"].title())}</h3><p>{esc(h["sub"])}</p></div>{mph}</div>
  <p class="instr">{route}</p>
  <figure class="lv">{lv}<figcaption>{lane_cap}</figcaption></figure>
  <figure class="dv">{d["svg"]}<figcaption>From above, with you driving up the page. Your route in solid blue, other choices dashed, amber = signal here.</figcaption></figure>
  <ul class="opts">{"".join(opts)}</ul>
  {note}
  <div class="meta"><span class="dist">{dist}</span><details><summary>Aerial photo</summary><img src="img/{name}.jpg" alt="Aerial photo of {esc(h["title"].title())} with the route drawn on." loading="lazy"></details><a class="sv" href="{SV(*sv)}" target="_blank" rel="noopener">Street View ↗</a></div>
</article>'''

def section(key):
    out = []
    for c in CARDS[key]:
        if isinstance(c, str):
            text, k = c.split('|'); out.append(f'<p class="stretch"><b class="k">{k}</b><span>{text}</span></p>')
        else: out.append(card(*c))
    return '\n'.join(out)

tpl = open(ROOT + 'tools/page_template.html').read()
page = tpl.replace('{{START}}', section('start')).replace('{{EXTA}}', section('a')).replace('{{EXTB}}', section('b'))
open(ROOT + 'index.html', 'w').write(page); print('page', len(page)//1024, 'KB')
