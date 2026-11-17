import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aer
OUTDIR = '/home/user/scotloand-trip/bishopbriggs-test-route/img/'
BLUE = (29, 95, 209); ORANGE = (240, 128, 30); MAGENTA = (214, 58, 166); TEAL = (0, 150, 136); GREY = (120, 120, 120)
SIGN = (0, 112, 60); YEL = (255, 210, 0); INK = (17, 22, 20); AMBER = (255, 176, 0); RED = (200, 35, 30)
def F(sz, bold=True): return aer.font(sz, bold)

def brg(a, b):
    (lo1, la1), (lo2, la2) = a, b
    y = math.sin(math.radians(lo2-lo1))*math.cos(math.radians(la2))
    x = math.cos(math.radians(la1))*math.sin(math.radians(la2))-math.sin(math.radians(la1))*math.cos(math.radians(la2))*math.cos(math.radians(lo2-lo1))
    return (math.degrees(math.atan2(y, x))+360) % 360
def dest(p, bearing, dist_m):
    lat = math.radians(p[1]); b = math.radians(bearing)
    return (p[0] + dist_m*math.sin(b)/(111320*math.cos(lat)), p[1] + dist_m*math.cos(b)/110540)
def arc(cen, r_m, b0, b1, step=10):
    span = (b1-b0) % 360; n = max(2, int(span/step)+1)
    return [dest(cen, b0+span*i/(n-1), r_m) for i in range(n)]
def sub_arc(ring, cen, b0, b1):
    span = (b1-b0) % 360
    pts = sorted(((brg(cen, p)-b0) % 360, p) for p in ring)
    return [p for d, p in pts if d <= span]

def dashes(P, L):
    out, cur, acc, on = [], [P[0]], 0.0, True
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        seg = math.hypot(x2-x1, y2-y1); t = 0.0
        while seg - t > 1e-6:
            step = min(L-acc, seg-t); t += step; acc += step
            pt = (x1+(x2-x1)*t/seg, y1+(y2-y1)*t/seg)
            if on: cur.append(pt)
            if acc >= L - 1e-6:
                if on and len(cur) > 1: out.append(cur)
                on = not on; acc = 0.0; cur = [pt]
    if on and len(cur) > 1: out.append(cur)
    return out

class Scene:
    def __init__(self, bbox, z=19, heading=None, **kw):
        self.img = aer.fetch_box(*bbox, z=z); self.bbox = bbox
        a = self.img.px((bbox[0], bbox[1])); b = self.img.px((bbox[2], bbox[3]))
        self.crop = (int(min(a[0], b[0])), int(min(a[1], b[1])), int(max(a[0], b[0])), int(max(a[1], b[1])))
        self.d = self.img.d
    def island(self, *a, **k): pass
    def P(self, segs):
        """segs: list of (lonlat_points, offset_m). Offset positive = right of travel."""
        out = []
        for pts, off in segs:
            out += self.offpx(pts, off)
        return out
    def offpx(self, pts, off_m):
        P = [self.img.px(p) for p in pts]; m = self.img.mpp(pts[0][1]); o = off_m/m; res = []
        for i, (x, y) in enumerate(P):
            a = P[max(i-1, 0)]; b = P[min(i+1, len(P)-1)]
            dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
            res.append((x + (-dy/L)*o, y + (dx/L)*o))
        return res
    def path(self, P, col, w=13, dash=None, arrow=True, alpha=235):
        rgba = col + (alpha,)
        segs = dashes(P, dash) if dash else [P]
        for s in segs: self.d.line(s, fill=(255, 255, 255, 235), width=w+6, joint='curve')
        for s in segs: self.d.line(s, fill=rgba, width=w, joint='curve')
        if arrow:
            (x1, y1), (x2, y2) = P[-2], P[-1]; a = math.atan2(y2-y1, x2-x1); L = w*1.9; W = w*1.35
            tip = (x2+math.cos(a)*L, y2+math.sin(a)*L)
            l = (x2+math.sin(a)*W, y2-math.cos(a)*W); r = (x2-math.sin(a)*W, y2+math.cos(a)*W)
            self.d.polygon([tip, l, r], fill=rgba, outline=(255, 255, 255, 235))
    def pt(self, lonlat, off=None):
        return self.img.px(lonlat)
    def label(self, xy, text, col=INK, bg=(255, 255, 255), border=None, sz=26, anchor='lm', dot=None, pad=8):
        if not hasattr(self, 'boxes'): self.boxes = []
        f = F(sz); x, y = xy
        lines = text.split('\n'); tw = max(self.d.textlength(t, font=f) for t in lines); th = sz*1.18*len(lines)
        if anchor[0] == 'm': x -= tw/2
        elif anchor[0] == 'r': x -= tw
        if anchor[1] == 'm': y -= th/2
        elif anchor[1] == 'b': y -= th
        cx0, cy0, cx1, cy1 = self.crop
        x = min(max(x, cx0+pad+6), cx1-tw-pad-6); y = min(max(y, cy0+pad+6), cy1-th-pad-6)
        def ov(b):
            return any(not (b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]) for o in self.boxes)
        box = [x-pad, y-pad, x+tw+pad, y+th+pad]
        for k in range(1, 40):
            if not ov(box): break
            dyk = ((k+1)//2)*14*(1 if k % 2 else -1)
            yy = min(max(y+dyk, cy0+pad+6), cy1-th-pad-6); box = [x-pad, yy-pad, x+tw+pad, yy+th+pad]
        x, y = box[0]+pad, box[1]+pad
        self.boxes.append(box)
        if dot:
            bx = min(max(dot[0], box[0]), box[2]); by = min(max(dot[1], box[1]), box[3])
            self.d.line([dot, (bx, by)], fill=(255, 255, 255, 230), width=4)
            self.d.ellipse([dot[0]-7, dot[1]-7, dot[0]+7, dot[1]+7], fill=(255, 255, 255, 255), outline=col+(255,), width=4)
        self.d.rounded_rectangle(box, radius=8, fill=bg+(242,), outline=(border or col)+(255,), width=3)
        for i, t in enumerate(lines): self.d.text((x, y+i*sz*1.18), t, fill=col+(255,), font=f)
        return box
    def signal(self, xy, kind, text=None, anchor='mm'):
        t = {'L': '◀ SIGNAL LEFT', 'R': 'SIGNAL RIGHT ▶', 'N': 'NO SIGNAL'}[kind] if text is None else text
        return self.label(xy, t, col=INK, bg=AMBER if kind != 'N' else (235, 235, 235), border=INK, sz=26, anchor=anchor)
    def render(self, name, head, legend, note=None, credit='Photo: Esri World Imagery (Maxar, Earthstar Geographics). Lanes and exits: OpenStreetMap.'):
        photo = self.img.finish().crop(self.crop)
        W = photo.width
        def wrap(d, text, f, width):
            out = []
            for para in text.split('\n'):
                words = para.split(' '); line = ''
                for wd in words:
                    t = (line + ' ' + wd).strip()
                    if d.textlength(t, font=f) <= width: line = t
                    else: out.append(line); line = wd
                out.append(line)
            return out
        tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        fr = F(27); rl = wrap(tmp, head['route'], fr, W-64)
        hh = 128 + 22 + len(rl)*34 + 10
        H = Image.new('RGB', (W, hh), SIGN); d = ImageDraw.Draw(H)
        d.ellipse([20, 20, 100, 100], fill=(255, 255, 255)); n = head['num']; f = F(44)
        d.text((60-d.textlength(n, font=f)/2, 32), n, fill=SIGN, font=f)
        avail = W - 120 - (124 if head.get('mph') else 20)
        ts = 40
        while ts > 22 and d.textlength(head['title'], font=F(ts)) > avail: ts -= 1
        ss = 24
        while ss > 15 and d.textlength(head['sub'], font=F(ss, False)) > avail: ss -= 1
        d.text((120, 18 + (40-ts)//2), head['title'], fill=(255, 255, 255), font=F(ts))
        d.text((120, 70), head['sub'], fill=(225, 240, 230), font=F(ss, False))
        sp = head.get('mph')
        if sp:
            cx, cy, R = W-62, 60, 42
            d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(255, 255, 255), outline=(212, 33, 27), width=10)
            f2 = F(32); d.text((cx-d.textlength(sp, font=f2)/2, cy-20), sp, fill=INK, font=f2)
        d.rounded_rectangle([16, 124, W-16, hh-12], radius=10, fill=(255, 255, 255))
        for i, ln in enumerate(rl): d.text((32, 136+i*34), ln, fill=INK, font=fr)
        # legend: two lines per option
        f1 = F(26); f2b = F(23, False)
        blocks = []
        for r in legend:
            l2 = wrap(tmp, r.get('line2') or ('Lane ' + r['lane'] + '  ·  Approach: ' + r['in'] + '  ·  Leave: ' + r['out']), f2b, W-110)
            blocks.append((r, l2))
        lh = 20 + sum(44 + 30*len(l2) + 14 for r, l2 in blocks) + (len(wrap(tmp, note, F(22), W-44))*30 + 16 if note else 0)
        L = Image.new('RGB', (W, lh), (255, 255, 255)); d2 = ImageDraw.Draw(L); y = 14
        for r, l2 in blocks:
            h = 44 + 30*len(l2)
            if r.get('primary'): d2.rounded_rectangle([10, y-4, W-10, y+h+4], radius=10, fill=(228, 238, 252))
            c = r['color']; d2.line([24, y+22, 76, y+22], fill=c, width=12)
            if r.get('dash'): d2.line([44, y+22, 54, y+22], fill=(255, 255, 255), width=12)
            d2.text((92, y+6), r['told'], fill=INK, font=f1)
            for j, ln in enumerate(l2): d2.text((92, y+42+j*30), ln, fill=(40, 48, 44), font=f2b)
            y += h + 14
        if note:
            for j, ln in enumerate(wrap(tmp, note, F(22), W-44)): d2.text((22, y+4+j*30), ln, fill=(160, 45, 20), font=F(22))
        C = Image.new('RGB', (W, 36), (240, 242, 240)); d3 = ImageDraw.Draw(C)
        d3.text((14, 9), credit, fill=(95, 105, 100), font=F(16, False))
        out = Image.new('RGB', (W, hh+photo.height+lh+36), (255, 255, 255))
        out.paste(H, (0, 0)); out.paste(photo, (0, hh)); out.paste(L, (0, hh+photo.height)); out.paste(C, (0, hh+photo.height+lh))
        out.save(OUTDIR+name, quality=82, optimize=True, progressive=True)
        print(name, out.size, os.path.getsize(OUTDIR+name)//1024, 'KB')
        return out
def load_ways(files):
    W = {}
    for f in files:
        for e in json.load(open(f)):
            g = e['geojson']; c = g['coordinates'][0][:-1] if g['type'] == 'Polygon' else g['coordinates']
            W[e['osm_id']] = [tuple(p) for p in c]
    return W

# ---------- generic helpers for lane-accurate junction scenes ----------
LW = 3.2
def load_all():
    W, T = {}, {}
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'osm')
    for f in ['ways1.json', 'ways2.json', 'ways3.json', 's_20_Glasgow_Road.json', 's_21_Torrance.json', 's_25_peelpark.json', 's_3_kilsyth.json', 's_26_k1ring.json']:
        try: data = json.load(open(os.path.join(D, f)))
        except Exception: continue
        for e in data:
            if e.get('osm_type') not in (None, 'way'): continue
            g = e['geojson']; c = g['coordinates'][0][:-1] if g['type'] == 'Polygon' else g['coordinates']
            W[e['osm_id']] = [tuple(p) for p in c]; T[e['osm_id']] = e.get('extratags') or {}
    for r in json.load(open(os.path.join(D, 'a803_all.json'))):
        W[r['id']] = [tuple(p) for p in r['c']]; T[r['id']] = r['t']
    return W, T
def lanes_info(t, forward):
    oneway = t.get('oneway') == 'yes'
    n = int(t.get('lanes', '1' if oneway else '2'))
    if oneway:
        ours, total, turns = n, n, (t.get('turn:lanes') or t.get('turn:lanes:forward'))
    else:
        lf, lb = t.get('lanes:forward'), t.get('lanes:backward')
        if lf or lb:
            lf = int(lf) if lf else n-int(lb); lb = int(lb) if lb else n-lf
        else:
            lf = lb = max(1, n//2)
        ours, total = (lf if forward else lb), n
        turns = t.get('turn:lanes:forward' if forward else 'turn:lanes:backward')
    offs = [-total*LW/2 + (i+0.5)*LW for i in range(ours)]
    return offs, (turns.split('|') if turns else None)
def way_pts(W, wid, d): return W[wid] if d > 0 else list(reversed(W[wid]))
def chain(S, W, T, links):
    """links: [(wid, dir, lane)] lane = index from left, -1 = rightmost, None = centre of our lanes"""
    out = []
    for wid, d, lane in links:
        offs, _ = lanes_info(T[wid], d > 0)
        if lane is None: off = sum(offs)/len(offs)
        else: off = offs[lane] if lane < len(offs) else offs[-1]
        out += S.offpx(way_pts(W, wid, d), off)
    return out
def back_point(pts, back_m):
    """walk back from the last point of a lon/lat polyline"""
    rem = back_m
    for i in range(len(pts)-1, 0, -1):
        a, b = pts[i], pts[i-1]
        seg = math.hypot((b[0]-a[0])*111320*math.cos(math.radians(a[1])), (b[1]-a[1])*110540)
        if seg >= rem:
            t = rem/seg; return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t), brg(b, a)
        rem -= seg
    return pts[0], brg(pts[0], pts[-1])
GLYPH = {'left': '←', 'through': '↑', 'right': '→', 'slight_left': '↖', 'slight_right': '↗', 'none': '•', '': '•', 'reverse': '↶'}
def lane_pills(S, W, T, wid, d, back_m=16, use=(), turns_override=None, sz=26):
    pts = way_pts(W, wid, d); offs, turns = lanes_info(T[wid], d > 0)
    turns = turns_override or turns or ['?']*len(offs)
    p, b = back_point(pts, back_m)
    if getattr(S, 'svg', False):
        S.lane_pills(pts, offs, turns, use, p, b); return p, b, offs
    placed = []
    for i, (off, tr) in enumerate(zip(offs, turns)):
        q = dest(p, (b+90) % 360, off); xy = S.img.px(q)
        g = ' '.join(GLYPH.get(x, '?') for x in tr.split(';'))
        on = i in use
        f = F(sz); tw = S.d.textlength(g, font=f); box = [xy[0]-tw/2-9, xy[1]-sz/2-8, xy[0]+tw/2+9, xy[1]+sz/2+6]
        S.d.rounded_rectangle(box, radius=7, fill=((29, 95, 209, 245) if on else (255, 255, 255, 235)), outline=(255, 255, 255, 255) if on else (40, 40, 40, 255), width=3)
        S.d.text((xy[0]-tw/2, xy[1]-sz/2-3), g, fill=(255, 255, 255, 255) if on else (20, 20, 20, 255), font=f)
        placed.append(box)
    if not hasattr(S, 'boxes'): S.boxes = []
    S.boxes += placed
    return p, b, offs
def lights(S, lonlat, sz=1.0):
    if getattr(S, 'svg', False): return S.lights(lonlat)
    x, y = S.img.px(lonlat); w, h = 26*sz, 66*sz
    S.d.rounded_rectangle([x-w/2, y-h/2, x+w/2, y+h/2], radius=6, fill=(20, 20, 20, 255), outline=(255, 255, 255, 255), width=3)
    for i, c in enumerate([(230, 40, 30), (250, 175, 0), (40, 190, 70)]):
        cy = y-h/2+11*sz+i*21*sz; r = 7.5*sz
        S.d.ellipse([x-r, cy-r, x+r, cy+r], fill=c+(255,))
    if not hasattr(S, 'boxes'): S.boxes = []
    S.boxes.append([x-w/2, y-h/2, x+w/2, y+h/2])
def bbox_around(lon, lat, w_m, h_m):
    dl = w_m/2/(111320*math.cos(math.radians(lat))); dt = h_m/2/110540
    return (lon-dl, lat+dt, lon+dl, lat-dt)
