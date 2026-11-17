import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import load_all, way_pts, brg
from PIL import Image, ImageDraw, ImageFont
import subprocess
W, T = load_all()
def hav(a, b):
    R = 6371000; (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2); dp = p2-p1; dl = math.radians(lo2-lo1)
    return 2*R*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
A = [(1221577807, 1), (1221577802, -1), (1221577800, -1), (249121829, -1), (1221577799, -1), (1221577801, -1), (1221577797, -1), (238095555, -1), (238095556, -1),
     (238093291, -1), (238093293, -1), (238093294, -1), (238093297, -1), (238093299, -1), (238093292, -1), (107204091, -1), (247132527, -1), (1133499062, -1),
     (257658423, -1), (1133499075, -1), (272344765, -1), (257658422, -1), (1447690658, 1), (249121830, -1), (257590895, -1), (31000816, -1), (31000815, -1),
     (536214137, -1), (4470843, -1), (31000828, -1)]
B = [(1221577806, 1), (32395, 1), (107204097, 1), (1311050665, 1), (1123138917, 1), (1123138913, 1), (4272906, 1), (34083614, 1), (32267, 1), (108960740, 1),
     (244450778, 1), (1091042230, 1), (55797460, 1), (1217589583, 1), (239507310, 1), (1204558500, 1), (246568459, 1), (1327381426, 1), (1546940010, 1),
     (1204558498, 1), (1217589582, 1), (1324500077, 1), (35536504, 1), (1324500076, 1), (35536505, 1), (1324500075, 1)]
def build(ch):
    pts = []
    for w, d in ch:
        if w not in W: print('missing', w); continue
        pts += way_pts(W, w, d)
    return pts
PA, PB = build(A), build(B)
def cum(pts):
    c = [0]
    for a, b in zip(pts, pts[1:]): c.append(c[-1]+hav(a, b))
    return c
def at(pts, c, p):
    i = min(range(len(pts)), key=lambda k: hav(pts[k], p)); return c[i]
CA, CB = cum(PA), cum(PB)
JA = {'A1': W[1221577802][0], 'A2': W[1221577801][0], 'A3': W[238095556][0], 'A4': W[238093294][0], 'A4b': W[238093299][0], 'A5': W[1133499075][0],
      'A6': W[249121830][0], 'A7': W[4470843][0]}
JB = {'B1': W[1123138917][-1], 'B2': W[55797460][0], 'B3': W[1204558500][-1], 'B4': W[1324500075][-1]}
dist = {}
for k, p in JA.items(): dist[k] = round(at(PA, CA, p)); 
for k, p in JB.items(): dist[k] = round(at(PB, CB, p))
dist['A_total'] = round(CA[-1]); dist['B_total'] = round(CB[-1])
dist['B_30mph'] = round(at(PB, CB, W[108960740][0])); dist['A_30mph'] = round(at(PA, CA, W[247132527][-1]))
print(dist)
json.dump(dict(dist=dist, A=PA, B=PB), open('/home/user/scotloand-trip/bishopbriggs-test-route/data/extensions.json', 'w'))
# overview at z15 from tiles
start = json.load(open('/home/user/scotloand-trip/bishopbriggs-test-route/data/route-geometry.json'))
z = 15
def t(lon, lat):
    n = 2**z; return (lon+180)/360*n, (1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
allp = PA + PB + [tuple(p) for p in start['main']]
lon0 = min(p[0] for p in allp)-0.004; lon1 = max(p[0] for p in allp)+0.004; lat0 = max(p[1] for p in allp)+0.002; lat1 = min(p[1] for p in allp)-0.002
xa, ya = t(lon0, lat0); xb, yb = t(lon1, lat1); x0, x1, y0, y1 = int(xa), int(xb), int(ya), int(yb)
UA = 'route-study-script/1.0 (personal driving-route study)'
im = Image.new('RGB', ((x1-x0+1)*256, (y1-y0+1)*256), (235, 235, 235))
for x in range(x0, x1+1):
    for y in range(y0, y1+1):
        f = f'tiles/{z}_{x}_{y}.png'
        if not os.path.exists(f): subprocess.run(['curl', '-sS', '-m', '30', '-A', UA, '-o', f, f'https://tile.openstreetmap.org/{z}/{x}/{y}.png'], check=True)
        im.paste(Image.open(f).convert('RGB'), ((x-x0)*256, (y-y0)*256))
S = 2; im = im.resize((im.width*S, im.height*S), Image.LANCZOS); d = ImageDraw.Draw(im)
px = lambda p: (((t(*p)[0])-x0)*256*S, ((t(*p)[1])-y0)*256*S)
fnt = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
def line(pts, col, w):
    P = [px(p) for p in pts]; d.line(P, fill=(255, 255, 255), width=w+8, joint='curve'); d.line(P, fill=col, width=w, joint='curve')
line(PB, (196, 74, 16), 18); line(PA, (29, 95, 209), 18); line([tuple(p) for p in start['main']], (17, 24, 39), 18)
def mark(p, lab, col, dx=0, dy=0):
    x, y = px(p); x += dx; y += dy; f = fnt(40); tw = d.textlength(lab, font=f); r = max(32, tw/2+14)
    d.rounded_rectangle([x-r, y-28, x+r, y+28], radius=28, fill=col, outline=(255, 255, 255), width=3); d.text((x-tw/2, y-24), lab, fill=(255, 255, 255), font=f)
mark(tuple(start['access']), 'START', (17, 24, 39), 40, -30)
mark(tuple(start['centres']['cadder']), '4', (17, 24, 39), -30, 0)
offs = {'A1': (-80, 20), 'A2': (-80, 0), 'A3': (-80, 0), 'A4': (-80, 0), 'A5': (-80, 0), 'A6': (-80, 0), 'A7': (-80, 0)}
for k, p in JA.items():
    if k == 'A4b': continue
    mark(p, k, (29, 95, 209), *offs.get(k, (0, 0)))
for k, p in JB.items(): mark(p, k, (196, 74, 16), 0, -56)
# crop to route
P = [px(p) for p in allp]; L = max(0, min(x for x, y in P)-120); R = min(im.width, max(x for x, y in P)+120); Tt = max(0, min(y for x, y in P)-90); Bt = min(im.height, max(y for x, y in P)+90)
im = im.crop((int(L), int(Tt), int(R), int(Bt)))
if im.width > 1400: im = im.resize((1400, int(im.height*1400/im.width)), Image.LANCZOS)
d = ImageDraw.Draw(im); d.rectangle([0, im.height-30, im.width, im.height], fill=(245, 245, 245)); d.text((10, im.height-26), 'Map © OpenStreetMap contributors', fill=(80, 80, 80), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18))
im.convert('P', palette=Image.ADAPTIVE, colors=200).save('/home/user/scotloand-trip/bishopbriggs-test-route/img/overview-full.png', optimize=True)
print('overview', im.size, os.path.getsize('/home/user/scotloand-trip/bishopbriggs-test-route/img/overview-full.png')//1024, 'KB')
