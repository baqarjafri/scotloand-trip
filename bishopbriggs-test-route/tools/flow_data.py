import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import load_all, way_pts, brg
W, T = load_all()
def hav(a, b):
    R = 6371000; (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2); dp = p2-p1; dl = math.radians(lo2-lo1)
    return 2*R*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
def build(ch):
    pts = []
    for w, d in ch: pts += way_pts(W, w, d)
    return pts
ext = json.load(open('/home/user/scotloand-trip/bishopbriggs-test-route/data/extensions.json'))
start = json.load(open('/home/user/scotloand-trip/bishopbriggs-test-route/data/route-geometry.json'))
PS = [tuple(p) for p in start['main']]
PA = [tuple(p) for p in ext['A']] + build([(1133499078, -1), (6182163, 1), (46493560, 1), (46493559, 1), (46493485, 1), (46493484, 1), (202753583, 1)])
PB = [tuple(p) for p in ext['B']] + build([(32268, 1), (267223308, 1), (1324500074, 1), (267223306, 1)]) + [(-4.15040, 55.94292)] + build([(32269, 1), (108960743, 1)])
def cum(P):
    c = [0]
    for a, b in zip(P, P[1:]): c.append(c[-1]+hav(a, b))
    return c
CS, CA, CB = cum(PS), cum(PA), cum(PB)
def near(P, C, p): i = min(range(len(P)), key=lambda k: hav(P[k], p)); return C[i]
def at(P, C, d):
    d = max(0, min(d, C[-1]))
    for i in range(len(C)-1):
        if C[i+1] >= d:
            t = (d-C[i])/((C[i+1]-C[i]) or 1); a, b = P[i], P[i+1]; return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)
    return P[-1]
def sv(P, C, d, back=False, gap=45):
    j = at(P, C, d); q = at(P, C, d+gap if back else d-gap)
    return [round(q[1], 6), round(q[0], 6), round(brg(q, j))]
OFF = {'S': 0, 'A': 0.846, 'B': 0.846}
J = {  # name: (polyline key, junction lon/lat)
 'S0': ('S', start['access']), 'S1': ('S', start['centres']['cole']), 'S2': ('S', start['signals']), 'S3': ('S', start['centres']['lowmoss']), 'S4': ('S', start['centres']['cadder']),
 'A1': ('A', W[1221577802][0]), 'A2': ('A', W[1221577801][0]), 'A3': ('A', W[238095556][0]), 'A4': ('A', W[238093294][0]), 'A4b': ('A', W[238093299][0]),
 'A5': ('A', W[1133499075][0]), 'A5b': ('A', W[257658421][0]), 'A6': ('A', W[249121830][0]), 'A7': ('A', W[4470843][0]),
 'A8': ('A', (-4.23323, 55.88853)), 'A9': ('A', (-4.23385, 55.88020)), 'A10': ('A', (-4.23210, 55.87730)),
 'B1': ('B', W[1123138917][-1]), 'B2': ('B', W[55797460][0]), 'B3': ('B', W[1204558500][-1]), 'B4': ('B', W[1324500075][-1]),
 'B5': ('B', (-4.15040, 55.94292)), 'B6': ('B', W[108960743][0])}
PP = {'S': (PS, CS), 'A': (PA, CA), 'B': (PB, CB)}
out = {}
for k, (pk, p) in J.items():
    P, C = PP[pk]; d = near(P, C, tuple(p))
    out[k] = dict(km=round(OFF[pk] + d/1000 - (0.045 if pk == 'S' else 0), 2), out=sv(P, C, d), back=sv(P, C, d, back=True))
# special cases
out['S0']['out'] = [55.924472, -4.199620, 262]; out['S0']['back'] = [55.924483, -4.199844, 82]; out['S0']['km'] = 0.0
out['S4']['back_a'] = sv(PA, CA, 0, back=True, gap=60); out['S4']['back_a'][2] = round(brg((out['S4']['back_a'][1], out['S4']['back_a'][0]), tuple(start['centres']['cadder'])))
out['S4']['back_b'] = sv(PB, CB, 0, back=True, gap=70); out['S4']['back_b'][2] = round(brg((out['S4']['back_b'][1], out['S4']['back_b'][0]), tuple(start['centres']['cadder'])))
print(json.dumps(out, indent=0)[:3000])
print('A total from centre %.2f km, B total %.2f km' % (0.846 + CA[-1]/1000, 0.846 + CB[-1]/1000))
json.dump(out, open('/home/user/scotloand-trip/bishopbriggs-test-route/data/flow-points.json', 'w'))
