import json, math, os, html
from PIL import ImageFont
DIAG = '/home/user/scotloand-trip/bishopbriggs-test-route/diag/'
os.makedirs(DIAG, exist_ok=True)
_F = {}
def tw(text, fs, bold=True):
    k = (fs, bold)
    if k not in _F: _F[k] = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 100)
    return _F[k].getlength(text) * fs / 100 * 0.93
CMAP = {(29, 95, 209): 'var(--c-route)', (240, 128, 30): 'var(--c-org)', (214, 58, 166): 'var(--c-mag)', (120, 120, 120): 'var(--c-grey)',
        (17, 22, 20): 'var(--fg)', (200, 35, 30): 'var(--c-red)', (0, 150, 136): 'var(--c-teal)'}
def C(c): return CMAP.get(tuple(c[:3]), 'var(--fg)')
esc = lambda s: html.escape(s, quote=True)
class _Img:
    def __init__(self, sc): self.sc = sc
    def px(self, p): return self.sc.px(p)
    def mpp(self, lat): return 1/self.sc.s
class SvgScene:
    svg = True
    def __init__(self, bbox, heading=0, **kw):
        lon0, lat0, lon1, lat1 = bbox
        self.c = ((lon0+lon1)/2, (lat0+lat1)/2); self.h = math.radians(heading)
        wm = abs(lon1-lon0)*111320*math.cos(math.radians(self.c[1])); hm = abs(lat1-lat0)*110540
        self.s = 5.98; self.W, self.H = int(wm*self.s), int(hm*self.s)
        self.crop = (0, 0, self.W, self.H); self.img = _Img(self); self.ops = []; self.roads = []; self.islands = []; self.boxes = []; self.lanes_rec = None; self.lane_tags = None
    def px(self, p):
        x = (p[0]-self.c[0])*111320*math.cos(math.radians(self.c[1])); y = (p[1]-self.c[1])*110540
        xr = x*math.cos(self.h) - y*math.sin(self.h); yr = x*math.sin(self.h) + y*math.cos(self.h)
        return (self.W/2 + xr*self.s, self.H/2 - yr*self.s)
    def pt(self, p, off=None): return self.px(p)
    def offpx(self, pts, off_m):
        P = [self.px(p) for p in pts]; o = off_m*self.s; res = []
        for i, (x, y) in enumerate(P):
            a = P[max(i-1, 0)]; b = P[min(i+1, len(P)-1)]
            dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
            res.append((x + (-dy/L)*o, y + (dx/L)*o))
        return res
    def P(self, segs):
        out = []
        for pts, off in segs: out += self.offpx(pts, off)
        return out
    def island(self, lonlat, r_m): self.islands.append((self.px(lonlat), r_m*self.s))
    def path(self, P, col, w=13, dash=None, arrow=True, alpha=235):
        sw = 19 if w >= 13 else 13
        self.roads.append(P)
        self.ops.append(('path', P, C(col), sw, bool(dash), arrow))
    def label(self, xy, text, col=(17, 22, 20), bg=(255, 255, 255), border=None, sz=26, anchor='lm', dot=None, pad=9):
        fs = 34
        SKIP = ('LEFT LANE', 'RIGHT LANE', 'A: LEFT', 'B: RIGHT', 'Stay in', 'Stay LEFT', 'Move to', 'RIGHT lane', 'LEFT lane', 'Single lane', 'Lane arrows not', 'NO SIGNAL', 'GIVE WAY')
        if text.startswith(SKIP): return [0, 0, 0, 0]
        lines = text.split('\n'); w = max(tw(t, fs) for t in lines); h = fs*1.2*len(lines)
        x, y = xy
        if anchor[0] == 'm': x -= w/2
        elif anchor[0] == 'r': x -= w
        if anchor[1] == 'm': y -= h/2
        elif anchor[1] == 'b': y -= h
        x = min(max(x, pad+3), self.W-w-pad-3); y = min(max(y, pad+3), self.H-h-pad-3)
        def ov(b): return any(not (b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]) for o in self.boxes)
        box = [x-pad, y-pad, x+w+pad, y+h+pad]
        for k in range(1, 50):
            if not ov(box): break
            dy = ((k+1)//2)*16*(1 if k % 2 else -1); yy = min(max(y+dy, pad+3), self.H-h-pad-3); box = [x-pad, yy-pad, x+w+pad, yy+h+pad]
        self.boxes.append(box)
        amber = tuple(bg[:3]) == (255, 176, 0)
        self.ops.append(('label', box, lines, fs, C(col) if not amber else '#111111', 'var(--c-amber)' if amber else 'var(--d-label)', C(border or col) if not amber else '#111111', dot))
        return box
    def signal(self, xy, kind, text=None, anchor='mm'):
        t = {'L': '◀ SIGNAL LEFT', 'R': 'SIGNAL RIGHT ▶', 'N': 'NO SIGNAL'}[kind] if text is None else text
        return self.label(xy, t, bg=(255, 176, 0) if kind != 'N' else (235, 235, 235), border=(17, 22, 20), anchor=anchor)
    def lights(self, lonlat):
        x, y = self.px(lonlat); self.ops.append(('lights', x, y)); self.boxes.append([x-14, y-34, x+14, y+34])
    def lane_pills(self, pts, offs, turns, use, p, b):
        if self.lanes_rec is None: self.lanes_rec = dict(turns=turns, use=list(use), tags=self.lane_tags)
    def to_svg(self, title):
        xs, ys = [], []
        for P in self.roads:
            for x, y in P: xs.append(x); ys.append(y)
        for op in self.ops:
            if op[0] == 'label': xs += [op[1][0], op[1][2]]; ys += [op[1][1], op[1][3]]
        m = 50; X0 = max(min(xs)-m, 0); Y0 = max(min(ys)-m, 0); X1 = min(max(xs)+m, self.W); Y1 = min(max(ys)+m, self.H)
        if (X1-X0) < 0.62*(Y1-Y0):
            pad = (0.62*(Y1-Y0)-(X1-X0))/2; X0 -= pad; X1 += pad
        self.vb = (X0, Y0, X1, Y1)
        o = [f'<svg viewBox="{X0:.0f} {Y0:.0f} {X1-X0:.0f} {Y1-Y0:.0f}" role="img" aria-label="{esc(title)}" class="diag">',
             f'<rect x="{X0-5:.0f}" y="{Y0-5:.0f}" width="{X1-X0+10:.0f}" height="{Y1-Y0+10:.0f}" class="d-bg"/>']
        rw = 10.0*self.s
        for P in self.roads:
            o.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in P)}" class="d-road" stroke-width="{rw:.1f}"/>')
        for (x, y), r in self.islands:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(r, 3):.1f}" class="d-island"/>')
        for op in self.ops:
            if op[0] == 'path':
                _, P, col, sw, dash, arrow = op
                pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in P)
                o.append(f'<polyline points="{pts}" class="d-case" stroke-width="{sw+2.6:.1f}"' + (' stroke-dasharray="9 6"' if dash else '') + '/>')
                o.append(f'<polyline points="{pts}" style="stroke:{col}" class="d-line" stroke-width="{sw}"' + (' stroke-dasharray="9 6"' if dash else '') + '/>')
                if arrow and len(P) > 1:
                    (x1, y1), (x2, y2) = P[-2], P[-1]; a = math.atan2(y2-y1, x2-x1); L = sw*2.4; Wd = sw*1.6
                    tip = (x2+math.cos(a)*L, y2+math.sin(a)*L); l = (x2+math.sin(a)*Wd, y2-math.cos(a)*Wd); r = (x2-math.sin(a)*Wd, y2+math.cos(a)*Wd)
                    o.append(f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {l[0]:.1f},{l[1]:.1f} {r[0]:.1f},{r[1]:.1f}" style="fill:{col}" class="d-head"/>')
        for op in self.ops:
            if op[0] == 'lights':
                _, x, y = op
                o.append(f'<g class="d-lights"><rect x="{x-13:.1f}" y="{y-33:.1f}" width="26" height="66" rx="6"/><circle cx="{x:.1f}" cy="{y-20:.1f}" r="7.5" fill="#e6281e"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="#faaf00"/><circle cx="{x:.1f}" cy="{y+20:.1f}" r="7.5" fill="#28be46"/></g>')
        for op in self.ops:
            if op[0] == 'label':
                _, box, lines, fs, col, bg, border, dot = op
                if dot:
                    bx = min(max(dot[0], box[0]), box[2]); by = min(max(dot[1], box[1]), box[3])
                    o.append(f'<line x1="{dot[0]:.1f}" y1="{dot[1]:.1f}" x2="{bx:.1f}" y2="{by:.1f}" class="d-leader"/> <circle cx="{dot[0]:.1f}" cy="{dot[1]:.1f}" r="7" class="d-dot" style="stroke:{border}"/>')
                o.append(f'<rect x="{box[0]:.1f}" y="{box[1]:.1f}" width="{box[2]-box[0]:.1f}" height="{box[3]-box[1]:.1f}" rx="9" style="fill:{bg};stroke:{border}" class="d-lab"/>')
                for i, t in enumerate(lines):
                     o.append(f'<text x="{box[0]+9:.1f}" y="{box[1]+9+fs*0.92+i*fs*1.2:.1f}" font-size="{fs}" style="fill:{col}" class="d-text">{esc(t)}</text>')
        # heading arrow
        o.append('</svg>')
        return '\n'.join(o)
    def render(self, name, head, legend, note=None, credit=None):
        out = dict(name=name, head=head, note=note, lanes=self.lanes_rec,
                   legend=[dict(color=C(r['color']), told=r['told'], line2=r.get('line2') or ('Lane ' + r['lane'] + ' · Approach: ' + r['in'] + ' · Leave: ' + r['out']), primary=bool(r.get('primary')), dash=bool(r.get('dash'))) for r in legend],
                   svg=self.to_svg(head['title'].title()))
        json.dump(out, open(DIAG + name.rsplit('.', 1)[0] + '.json', 'w'))
        print('diag', name)
