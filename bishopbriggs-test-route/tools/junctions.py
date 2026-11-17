import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *
W, T = load_all()
def centre(c): return (sum(p[0] for p in c)/len(c), sum(p[1] for p in c)/len(c))
ONLY = sys.argv[1:]
def want(k): return not ONLY or k in ONLY
LEG = lambda color, told, line2, primary=False, dash=False: dict(color=color, told=told, lane='', **{'in': '', 'out': ''}, primary=primary, dash=dash, line2=line2)

# ===== 01 Gate + Cole Road roundabout =====
if want('j01'):
    C = centre(W[24910637]); ACC = (-4.199620, 55.924472); ACC_IN = (-4.199406, 55.924085)
    S = Scene(bbox_around(-4.20045, 55.92415, 150, 125))
    appr = [p for p in reversed(W[24910594]) if p[0] < ACC[0]]
    gate = S.offpx([ACC_IN, ACC], 0)
    a = S.offpx([ACC] + appr, -1.6)
    first = gate + a + S.P([(arc(C, 12.6, 95, 205), 0)]) + S.offpx(W[30738202][:4], -1.6)
    second = a + S.P([(arc(C, 9.4, 100, 345), 0)]) + S.offpx(list(reversed(W[8368975]))[:4], -1.6)
    S.path(second, ORANGE, w=11, dash=22)
    S.path(first, BLUE, w=15)
    g = S.img.px(ACC_IN); S.label((g[0]+40, g[1]+40), '◀ SIGNAL LEFT\nto leave the centre', bg=AMBER, border=INK, anchor='lm', dot=S.img.px(ACC))
    q = S.img.px(appr[len(appr)//2]); S.label((q[0]-10, q[1]-110), '◀ SIGNAL LEFT again\n(1st exit) 57 m ahead', bg=AMBER, border=INK, anchor='mm', dot=q)
    gw = S.img.px(dest(C, 75, 13)); S.label((gw[0]+60, gw[1]+70), 'GIVE WAY\nto your right', col=RED, anchor='lm', dot=gw)
    e1 = first[-1]; S.label((e1[0]+20, e1[1]+40), '1  Crosshill Rd to retail park', col=BLUE, anchor='lm')
    e2 = second[-1]; S.label((e2[0]+20, e2[1]-30), '2  Cole Road (60 mph)', col=ORANGE, anchor='lm')
    S.render('j01-gate-cole.jpg',
      head=dict(num='0·1', title='GATE + COLE ROAD ROUNDABOUT', sub='B819 Crosshill Road  ·  3 arms  ·  no lane markings', mph='40',
                route='YOUR ROUTE: turn LEFT out of the centre, then FIRST EXIT at the roundabout 57 m later. Signal left twice.'),
      legend=[LEG(BLUE, 'First exit  ·  YOUR ROUTE', 'Keep left. ◀ Signal left on approach and keep it on as you leave.', True),
              LEG(ORANGE, 'Second exit, right: Cole Road', 'Signal right ▶ on approach, keep right, ◀ signal left once past exit 1.', dash=True)],
      note='The first exit bends only ~20° left and looks like straight on. It is still the first exit: signal left.')

# ===== 02 Retail park lights =====
if want('j02'):
    J = (-4.204178, 55.923284)
    S = Scene(bbox_around(-4.20395, 55.92335, 140, 120))
    route = chain(S, W, T, [(30738202, 1, 0), (1427552262, 1, 0), (1427552263, 1, 0)])
    left = chain(S, W, T, [(30738202, 1, 0)]) + S.P([([J, dest(J, 153, 35)], -1.6)])
    S.path(left, MAGENTA, w=11, dash=22); S.path(route, BLUE, w=15)
    lp, lb, _ = lane_pills(S, W, T, 30738202, 1, back_m=12, use=(0,), turns_override=['through;left'])
    lights(S, dest(dest(J, 63, 14), 333, 7))
    q = S.img.px(dest(J, 63, 45)); S.signal((q[0]+30, q[1]-90), 'N', text='NO SIGNAL (straight on)\nGo on green only', anchor='mm')
    e = S.img.px(dest(J, 153, 35)); S.label((e[0]+20, e[1]+20), 'Retail park (Aldi, B&Q)', col=MAGENTA, anchor='lm')
    S.label((route[-1][0]+10, route[-1][1]+50), 'To Lowmoss Roundabout', col=BLUE, anchor='lm')
    S.render('j02-retail-lights.jpg',
      head=dict(num='2', title='RETAIL PARK TRAFFIC LIGHTS', sub='B819 Crosshill Road  ·  T-junction  ·  ≈270 m after the roundabout', mph='40',
                route='YOUR ROUTE: STRAIGHT ON. One lane. No signal. Stop on red, go on green when clear.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'Single lane. No signal. Watch for cars pulling out of the car park.', True),
              LEG(MAGENTA, 'Left into the retail park', '◀ Signal left on approach, slow down, check the left mirror for cyclists.', dash=True)],
      note='Coming back east: the road has two lanes here. Left lane = straight on to the centre, right lane = right into the retail park.')

# ===== 04 Cadder roundabout =====
if want('j04'):
    C = centre(W[32397])
    S = Scene(bbox_around(-4.21035, 55.92105, 160, 165))
    appr = [(31093556, -1, 0)]
    A = chain(S, W, T, appr + [(1221577804, 1, 0)]) + S.P([(arc(C, 19.0, 120, 192), 0)]) + chain(S, W, T, [(1221577807, 1, 0), (1221577800, -1, 0), (249121829, -1, 0)])
    B = chain(S, W, T, appr + [(1221577804, 1, 1)]) + S.P([(arc(C, 15.2, 118, 330), 0)]) + chain(S, W, T, [(1221577806, 1, 0), (32395, 1, 0)])
    S.path(B, ORANGE, w=14); S.path(A, BLUE, w=14)
    lp, lb, offs = lane_pills(S, W, T, 1221577804, 1, back_m=8, use=(0, 1))
    q = S.img.px(dest(lp, (lb+180) % 360, 45))
    S.label((q[0]+40, q[1]-60), 'A: LEFT lane\n◀ signal left', col=BLUE, anchor='lm', dot=S.img.px(dest(lp, (lb+270) % 360, 1.6)))
    S.label((q[0]+60, q[1]+60), 'B: RIGHT lane\nsignal right ▶', col=ORANGE, anchor='lm', dot=S.img.px(dest(lp, (lb+90) % 360, 1.6)))
    sp = S.img.px(dest(C, 245, 15.2)); S.label((sp[0]-60, sp[1]-140), 'B: ◀ SIGNAL LEFT\nonce past exit A', bg=AMBER, border=INK, anchor='mm', dot=sp)
    S.label((A[-1][0]+20, A[-1][1]-10), 'A  A803 south:\nBishopbriggs', col=BLUE, anchor='lm')
    S.label((B[-1][0]+20, B[-1][1]+10), 'B  A803 north:\nTorrance', col=ORANGE, anchor='lm')
    S.render('j04-cadder.jpg',
      head=dict(num='4', title='CADDER ROUNDABOUT  ·  A803', sub='End of Crosshill Road  ·  your route splits here', mph='40',
                route='Pick your lane where the road opens into two lanes. A (south) = LEFT lane, first exit. B (north) = RIGHT lane, second exit.'),
      legend=[LEG(BLUE, 'A: First exit, A803 south (Bishopbriggs)', 'LEFT lane (arrow ahead). ◀ Signal left on approach, keep it on.', True),
              LEG(ORANGE, 'B: Second exit, A803 north (Torrance)', 'RIGHT lane. Signal right ▶ on approach, keep right, ◀ signal left after exit A.', True)],
      note='Both exits are single lane. On B, check the left mirror and blind spot before you move left to leave.')

# ===== A1 Cadder Road / Shell =====
if want('a1'):
    J = W[1221577802][0]
    S = Scene(bbox_around(-4.21125, 55.92070, 130, 140))
    route = chain(S, W, T, [(1221577807, 1, 0), (1221577802, -1, 0), (1221577800, -1, 0), (249121829, -1, 0)])
    right = chain(S, W, T, [(1221577807, 1, 0), (1221577802, -1, 1)]) + S.P([([J, dest(J, 296, 40)], -1.6)])
    S.path(right, MAGENTA, w=11, dash=22); S.path(route, BLUE, w=15)
    lane_pills(S, W, T, 1221577802, -1, back_m=10, use=(0,))
    e = S.img.px(dest(J, 296, 40)); S.label((e[0]-20, e[1]-40), 'Side road (20 mph)', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south', col=BLUE, anchor='lm')
    q = S.img.px(dest(J, 30, 35)); S.label((q[0]+70, q[1]+10), 'Stay in the\nLEFT lane', col=BLUE, anchor='lm', dot=q)
    S.render('a1-cadder-road.jpg',
      head=dict(num='A1', title='SIDE ROAD BY SHELL LOWMOSS', sub='A803 Kirkintilloch Road  ·  ≈70 m after Cadder Roundabout', mph='40',
                route='STRAIGHT ON: stay in the LEFT lane. The right lane opens up for the right turn only.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'LEFT lane. No signal. Watch for cars turning into Shell on your left.', True),
              LEG(MAGENTA, 'Right into the side road', 'Signal right ▶, move into the right lane, wait for a gap in oncoming traffic.', dash=True)])

# ===== A2 Westerhill Road lights =====
if want('a2'):
    J = W[1221577801][0]
    S = Scene(bbox_around(-4.21315, 55.91890, 130, 150))
    route = chain(S, W, T, [(1221577799, -1, 1), (1221577801, -1, 1), (1221577797, -1, 0), (238095555, -1, 0)])
    left = chain(S, W, T, [(1221577799, -1, 0), (1221577801, -1, 0)]) + S.P([([J, dest(J, 118, 40)], -1.6)])
    S.path(left, MAGENTA, w=11, dash=22); S.path(route, BLUE, w=15)
    lp, lb, offs = lane_pills(S, W, T, 1221577801, -1, back_m=14, use=(1,))
    lights(S, dest(dest(lp, (lb+270) % 360, 10), lb, 9))
    e = S.img.px(dest(J, 118, 40)); S.label((e[0]+10, e[1]+40), 'Westerhill Road', col=MAGENTA, anchor='lm')
    q = S.img.px(dest(lp, (lb+180) % 360, 40)); S.label((q[0]+60, q[1]-30), 'LEFT lane =\nleft only', col=MAGENTA, anchor='lm', dot=S.img.px(dest(dest(lp, (lb+180) % 360, 20), (lb+270) % 360, 3.2)))
    S.label((q[0]-260, q[1]+40), 'RIGHT lane =\nstraight on', col=BLUE, anchor='lm', dot=S.img.px(dest(lp, (lb+180) % 360, 24)))
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south', col=BLUE, anchor='lm')
    S.render('a2-westerhill-lights.jpg',
      head=dict(num='A2', title='WESTERHILL ROAD LIGHTS', sub='A803 Kirkintilloch Road  ·  T-junction  ·  ≈300 m after Cadder', mph='40',
                route='STRAIGHT ON: use the RIGHT lane. The left lane is LEFT ONLY into Westerhill Road. No signal. Go on green.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'RIGHT lane. No signal. After the lights the road narrows back to one lane.', True),
              LEG(MAGENTA, 'Left into Westerhill Road', 'LEFT lane. ◀ Signal left on approach.', dash=True)],
      note='Trap: as at Lowmoss, the left lane does not go straight on here.')

# ===== A3 Meadowburn =====
if want('a3'):
    J = W[238095556][0]
    S = Scene(bbox_around(-4.21560, 55.91650, 120, 140))
    route = chain(S, W, T, [(238095555, -1, 0), (238095556, -1, 0), (238093291, -1, 0)])
    right = chain(S, W, T, [(238095555, -1, 0), (238095556, -1, 1)]) + S.P([([J, dest(J, 296, 40)], -1.6)])
    S.path(right, MAGENTA, w=11, dash=22); S.path(route, BLUE, w=15)
    lane_pills(S, W, T, 238095556, -1, back_m=10, use=(0,))
    e = S.img.px(dest(J, 296, 40)); S.label((e[0]-10, e[1]-40), 'Meadowburn', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south', col=BLUE, anchor='lm')
    S.render('a3-meadowburn.jpg',
      head=dict(num='A3', title='MEADOWBURN JUNCTION', sub='A803 Kirkintilloch Road  ·  no lights  ·  ≈300 m after A2', mph='40',
                route='STRAIGHT ON: stay in the LEFT lane. The right lane is only for turning right into Meadowburn.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'LEFT lane. No signal.', True),
              LEG(MAGENTA, 'Right into Meadowburn', 'Signal right ▶, right lane, give way to oncoming traffic.', dash=True)])

# ===== A4+A5 Asda and Hilton Road lights =====
if want('a45'):
    J4 = W[238093294][0]; J5 = W[238093299][0]
    S = Scene(bbox_around(-4.21835, 55.91380, 150, 230))
    route = chain(S, W, T, [(238093291, -1, 0), (238093293, -1, 0), (238093294, -1, 0), (238093297, -1, 0), (238093299, -1, 0), (238093292, -1, 0), (107204091, -1, 0)])
    lft = chain(S, W, T, [(238093293, -1, 0), (238093294, -1, 0)]) + S.P([([J4, dest(J4, 114, 40)], -1.6)])
    r4 = chain(S, W, T, [(238093293, -1, 1), (238093294, -1, 2)]) + S.P([([J4, dest(J4, 284, 40)], -1.6)])
    r5 = chain(S, W, T, [(238093297, -1, 1), (238093299, -1, 2)]) + S.P([([J5, dest(J5, 298, 45)], -1.6)])
    for p, c in ((lft, ORANGE), (r4, MAGENTA), (r5, MAGENTA)): S.path(p, c, w=10, dash=20)
    S.path(route, BLUE, w=15)
    p4, b4, _ = lane_pills(S, W, T, 238093294, -1, back_m=12, use=(0,))
    p5, b5, _ = lane_pills(S, W, T, 238093299, -1, back_m=14, use=(0,))
    lights(S, dest(dest(p4, (b4+270) % 360, 12.5), b4, 8)); lights(S, dest(dest(p5, (b5+270) % 360, 12.5), b5, 10))
    e = S.img.px(dest(J4, 114, 40)); S.label((e[0]+10, e[1]+10), 'Asda', col=ORANGE, anchor='lm')
    e = S.img.px(dest(J4, 284, 40)); S.label((e[0]-10, e[1]-20), 'Side road', col=MAGENTA, anchor='rm')
    e = S.img.px(dest(J5, 298, 45)); S.label((e[0]-10, e[1]-20), 'Hilton Road', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south', col=BLUE, anchor='lm')
    q = S.img.px(dest(p4, (b4+180) % 360, 35)); S.label((q[0]+80, q[1]-20), 'Stay LEFT through\nboth sets of lights', col=BLUE, anchor='lm', dot=q)
    S.render('a45-asda-hilton.jpg',
      head=dict(num='A4', title='ASDA + HILTON ROAD LIGHTS', sub='A803  ·  two sets of lights ≈110 m apart  ·  Asda on your left', mph='40',
                route='STRAIGHT ON: LEFT lane through both sets of lights. The rightmost lane turns right at each one. No signal.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'LEFT lane (arrows ahead / ahead+left). The middle lane also goes ahead. No signal.', True),
              LEG(ORANGE, 'Left at the first lights (into Asda)', 'LEFT lane. ◀ Signal left.', dash=True),
              LEG(MAGENTA, 'Right at either set of lights', 'RIGHT lane. Signal right ▶. Hilton Road is the second one.', dash=True)])

# ===== A7 South Crosshill Road lights =====
if want('a7'):
    J = W[1133499075][0]
    S = Scene(bbox_around(-4.22415, 55.90690, 120, 160))
    route = chain(S, W, T, [(247132527, -1, 0), (1133499062, -1, 0), (257658423, -1, 0), (1133499075, -1, 0), (272344765, -1, 0)])
    left = chain(S, W, T, [(257658423, -1, 0), (1133499075, -1, 0)]) + S.P([([J, dest(J, 95, 40)], -1.6)])
    S.path(left, MAGENTA, w=11, dash=22); S.path(route, BLUE, w=15)
    p, b = back_point(way_pts(W, 1133499075, -1), 1)
    lights(S, dest(dest(p, (b+270) % 360, 8), b, 2))
    e = S.img.px(dest(J, 95, 40)); S.label((e[0]+10, e[1]+40), 'South Crosshill Road', col=MAGENTA, anchor='lm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south', col=BLUE, anchor='lm')
    q = S.img.px(dest(J, 15, 60)); S.signal((q[0]+50, q[1]), 'N', text='Single lane\nNO SIGNAL', anchor='lm')
    S.render('a7-crosshill-lights.jpg',
      head=dict(num='A5', title='SOUTH CROSSHILL ROAD LIGHTS', sub='A803  ·  30 mph from here  ·  T-junction', mph='30',
                route='STRAIGHT ON: one lane. No signal. The limit is now 30 mph: check your speed.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'Single lane. No signal. Stop on red.', True),
              LEG(MAGENTA, 'Left into South Crosshill Road', '◀ Signal left, check the left mirror for cyclists.', dash=True)])

# ===== A8/A9 Bishopbriggs Cross =====
if want('a89'):
    J9 = W[249121830][0]
    S = Scene(bbox_around(-4.22490, 55.90470, 160, 210))
    route = chain(S, W, T, [(272344765, -1, 0), (257658422, -1, 0), (1447690658, 1, 1), (249121830, -1, 1), (257590895, -1, 1), (31000816, -1, 0)])
    lft = chain(S, W, T, [(1447690658, 1, 0), (249121830, -1, 0)]) + S.P([([J9, dest(J9, 160, 40)], -1.6)])
    rgt = chain(S, W, T, [(1447690658, 1, 1), (249121830, -1, 2)]) + S.P([([J9, dest(J9, 290, 40)], -1.6)])
    S.path(lft, ORANGE, w=10, dash=20); S.path(rgt, MAGENTA, w=10, dash=20); S.path(route, BLUE, w=15)
    p9, b9, _ = lane_pills(S, W, T, 249121830, -1, back_m=10, use=(1,))
    lights(S, dest(dest(p9, (b9+270) % 360, 13), b9, 7))
    e = S.img.px(dest(J9, 160, 40)); S.label((e[0]+10, e[1]+30), 'Crowhill Road', col=ORANGE, anchor='lm')
    e = S.img.px(dest(J9, 290, 40)); S.label((e[0]-10, e[1]-30), 'Kenmure Avenue', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'A803 south: Auchinairn', col=BLUE, anchor='lm')
    q = S.img.px(dest(p9, (b9+180) % 360, 60)); S.label((q[0]+80, q[1]-20), 'Move to the\nMIDDLE lane', col=BLUE, anchor='lm', dot=q)
    S.render('a89-bishopbriggs-cross.jpg',
      head=dict(num='A6', title='BISHOPBRIGGS CROSS', sub='A803 at the station  ·  lights  ·  3 lanes on approach', mph='30',
                route='STRAIGHT ON: MIDDLE lane (arrow ahead). Left lane = Crowhill Road only. Right lane = Kenmure Avenue. No signal.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'MIDDLE lane. No signal. The road bears slightly left over the railway.', True),
              LEG(ORANGE, 'Left into Crowhill Road', 'LEFT lane. ◀ Signal left.', dash=True),
              LEG(MAGENTA, 'Right into Kenmure Avenue', 'RIGHT lane. Signal right ▶.', dash=True)],
      note='Just before this, Springfield Road (Morrisons) joins on your left at its own lights. Keep going straight.')

# ===== A11 Colston Road =====
if want('a11'):
    J = W[4470843][0]
    S = Scene(bbox_around(-4.23145, 55.89690, 130, 170))
    route = chain(S, W, T, [(536214137, -1, 0), (4470843, -1, 0), (31000828, -1, 0)])
    S.path(S.offpx(way_pts(W, 4470843, -1)[-3:] + [J, dest(J, 95, 40)], -1.6), ORANGE, w=10, dash=20)
    S.path(S.offpx(way_pts(W, 4470843, -1)[-3:] + [J, dest(J, 270, 40)], -1.6), MAGENTA, w=10, dash=20)
    S.path(route, BLUE, w=15)
    p, b = back_point(way_pts(W, 4470843, -1), 8)
    lights(S, dest(dest(p, (b+270) % 360, 8), b, 2))
    e = S.img.px(dest(J, 95, 40)); S.label((e[0]+10, e[1]+30), 'Colston Road (B812)', col=ORANGE, anchor='lm')
    e = S.img.px(dest(J, 270, 40)); S.label((e[0]-10, e[1]-40), 'Colston Road', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]+20, route[-1][1]-10), 'Springburn Road', col=BLUE, anchor='lm')
    q = S.img.px(dest(J, 0, 70)); S.signal((q[0]+40, q[1]), 'N', text='Lane arrows not mapped:\ncheck on the day', anchor='lm')
    S.render('a11-colston-road.jpg',
      head=dict(num='A7', title='COLSTON ROAD CROSSROADS', sub='A803 becomes Springburn Road  ·  lights', mph='30',
                route='STRAIGHT ON: left lane. No signal. Go on green when the box is clear.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'Left lane. No signal.', True),
              LEG(ORANGE, 'Left: Colston Road (B812)', '◀ Signal left.', dash=True),
              LEG(MAGENTA, 'Right: Colston Road', 'Signal right ▶, wait in the junction for a gap.', dash=True)])

# ===== B1 Torrance roundabout =====
if want('b1'):
    ring = [p for w in (247132533, 1123138909, 1123138911, 1123138910, 2425, 247132532) for p in W[w]]
    C = centre(ring)
    S = Scene(bbox_around(-4.20410, 55.92770, 140, 175))
    rad = sum(math.hypot((p[0]-C[0])*111320*math.cos(math.radians(C[1])), (p[1]-C[1])*110540) for p in ring)/len(ring)
    bin_ = brg(C, W[1123138917][-1]); bout = brg(C, W[1123138913][0])
    route = chain(S, W, T, [(107204097, 1, 0), (1311050665, 1, 1), (1123138917, 1, 1)]) + S.P([(arc(C, rad-1.6, bin_+12, bout-8), 0)]) + chain(S, W, T, [(1123138913, 1, 0), (4272906, 1, 0)])
    left = chain(S, W, T, [(1311050665, 1, 0), (1123138917, 1, 0)]) + S.P([(arc(C, rad+1.6, bin_+12, 318), 0), ([dest(C, 322, rad+2), dest(C, 330, rad+40)], -1.6)])
    rgt = chain(S, W, T, [(1123138917, 1, 1)]) + S.P([(arc(C, rad-1.6, bin_+12, 125), 0), ([dest(C, 130, rad+2), dest(C, 145, rad+40)], -1.6)])
    S.path(left, MAGENTA, w=10, dash=20); S.path(rgt, GREY, w=10, dash=20); S.path(route, BLUE, w=15)
    lane_pills(S, W, T, 1123138917, 1, back_m=10, use=(1,))
    sp = S.img.px(dest(C, 345, rad-1.6)); S.label((sp[0]-40, sp[1]-120), '◀ SIGNAL LEFT\nonce past Torrance Rd', bg=AMBER, border=INK, anchor='mm', dot=sp)
    q = S.img.px(dest(W[1311050665][0], 225, 10)); S.signal((q[0]+40, q[1]+40), 'N', text='NO SIGNAL on approach\nRIGHT lane', anchor='lm')
    e = S.img.px(dest(C, 330, rad+40)); S.label((e[0]-10, e[1]-20), '1  Torrance Road', col=MAGENTA, anchor='rm')
    S.label((route[-1][0]-20, route[-1][1]+40), '2  A803 to Kirkintilloch', col=BLUE, anchor='rm')
    e = S.img.px(dest(C, 145, rad+40)); S.label((e[0]+10, e[1]+20), '3  Cole Road', col=GREY, anchor='lm')
    S.render('b1-torrance.jpg',
      head=dict(num='B1', title='TORRANCE ROUNDABOUT', sub='A803 Kirkintilloch Road  ·  60 mph road  ·  ≈850 m after Cadder', mph='60',
                route='YOUR ROUTE: AHEAD, 2nd exit, A803 to Kirkintilloch. RIGHT lane. No signal on approach. ◀ Signal left once past Torrance Road.'),
      legend=[LEG(BLUE, 'Ahead (2nd exit)  ·  YOUR ROUTE', 'RIGHT lane. No signal on approach. ◀ Signal left after exit 1.', True),
              LEG(MAGENTA, 'First exit, left: Torrance Road', 'LEFT lane. ◀ Signal left on approach, keep it on.', dash=True),
              LEG(GREY, 'Third exit, right: Cole Road', 'RIGHT lane. Signal right ▶, ◀ signal left after exit 2.', dash=True)],
      note='Trap again: the left lane is LEFT ONLY. National speed limit roads meet here, so traffic arrives fast from your right.')

# ===== B3 New Lairdsland Road =====
if want('b3'):
    J = W[1204558500][-1]
    S = Scene(bbox_around(-4.16020, 55.94255, 150, 140))
    route = chain(S, W, T, [(55797460, 1, 0), (1217589583, 1, 0), (239507310, 1, 0), (1204558500, 1, 0), (246568459, 1, 0), (1327381426, 1, 0)])
    rgt = chain(S, W, T, [(239507310, 1, 1), (1204558500, 1, 1)]) + S.P([(way_pts(W, 1204558499, -1), -1.6)])
    S.path(rgt, MAGENTA, w=10, dash=20); S.path(route, BLUE, w=15)
    p, b, _ = lane_pills(S, W, T, 1204558500, 1, back_m=8, use=(0,))
    lights(S, dest(dest(p, (b+270) % 360, 10), b, 4))
    S.label((rgt[-1][0]+10, rgt[-1][1]+30), 'A806 New Lairdsland Rd', col=MAGENTA, anchor='lm')
    S.label((route[-1][0]-10, route[-1][1]-40), 'A803 Glasgow Road', col=BLUE, anchor='rm')
    S.render('b3-new-lairdsland.jpg',
      head=dict(num='B3', title='NEW LAIRDSLAND ROAD LIGHTS', sub='A803 Glasgow Road, Kirkintilloch  ·  30 mph', mph='30',
                route='STRAIGHT ON: LEFT lane (arrow ahead). Right lane = right turn into the A806. No signal.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'LEFT lane. No signal. Go on green.', True),
              LEG(MAGENTA, 'Right: A806 New Lairdsland Road', 'RIGHT lane. Signal right ▶.', dash=True)],
      note='On the way here the limit drops from 60 to 30 mph as you enter Kirkintilloch. Be at 30 by the signs.')

# ===== B4 Milton Road / Ledgate =====
if want('b4'):
    J = W[1324500075][-1]
    S = Scene(bbox_around(-4.15500, 55.94305, 140, 140))
    route = chain(S, W, T, [(1324500076, 1, 0), (35536505, 1, 0), (1324500075, 1, 0)]) + S.P([([J, dest(J, 97, 45)], -1.6)])
    lft = chain(S, W, T, [(1324500075, 1, 0)]) + S.P([(W[8232564][:3], -1.6)])
    rgt = chain(S, W, T, [(1324500075, 1, 1)]) + S.P([([J, dest(J, 168, 40)], -1.6)])
    S.path(lft, ORANGE, w=10, dash=20); S.path(rgt, MAGENTA, w=10, dash=20); S.path(route, BLUE, w=15)
    p, b, _ = lane_pills(S, W, T, 1324500075, 1, back_m=12, use=(0,))
    lights(S, dest(dest(p, (b+270) % 360, 10), b, 9))
    S.label((lft[-1][0]-10, lft[-1][1]-20), 'Milton Road (B757)', col=ORANGE, anchor='rm')
    e = S.img.px(dest(J, 168, 40)); S.label((e[0]+10, e[1]+20), 'Ledgate', col=MAGENTA, anchor='lm')
    S.label((route[-1][0]-10, route[-1][1]+50), 'A803 east', col=BLUE, anchor='rm')
    S.render('b4-milton-road.jpg',
      head=dict(num='B4', title='MILTON ROAD LIGHTS', sub='A803 Glasgow Road, Kirkintilloch town centre  ·  30 mph', mph='30',
                route='STRAIGHT ON: LEFT lane (arrows left + ahead). Right lane = Ledgate only. No signal.'),
      legend=[LEG(BLUE, 'Straight on  ·  YOUR ROUTE', 'LEFT lane. No signal. Watch for pedestrians in the town centre.', True),
              LEG(ORANGE, 'Left: Milton Road (B757)', 'LEFT lane. ◀ Signal left.', dash=True),
              LEG(MAGENTA, 'Right: Ledgate', 'RIGHT lane. Signal right ▶.', dash=True)])

# ===== B2 Peel Park roundabout =====
if want('b2'):
    C = (-4.16339, 55.940665)
    rad = max(math.hypot((p[0]-C[0])*111320*math.cos(math.radians(C[1])), (p[1]-C[1])*110540) for p in W[34083616])
    print('peel radius', round(rad, 1))
    S = Scene(bbox_around(C[0]-0.0003, C[1]-0.0001, 140, 150))
    appr = W[1091042230][-8:]
    bin_ = brg(C, appr[-1]); bout = brg(C, W[55797460][0])
    route = S.offpx(appr, -1.6) + S.P([(arc(C, rad+1.2, bin_+10, bout-6), 0)]) + S.offpx(W[55797460] + W[1217589583][1:], -1.6)
    alt = S.offpx(appr, -1.6) + S.P([(arc(C, rad-1.2, bin_+10, 100), 0), ([dest(C, 104, rad+2), dest(C, 108, rad+45)], -1.6)])
    S.path(alt, MAGENTA, w=10, dash=20); S.path(route, BLUE, w=15)
    q = S.img.px(back_point(appr, 30)[0]); S.label((q[0]+60, q[1]+30), '◀ SIGNAL LEFT on approach\n(1st exit = A803 ahead)', bg=AMBER, border=INK, anchor='lm', dot=q)
    gw = S.img.px(dest(C, bin_, rad+3)); S.label((gw[0]-40, gw[1]-90), 'GIVE WAY to your right', col=RED, anchor='rm', dot=gw)
    S.label((route[-1][0]-10, route[-1][1]-30), '1  A803 Glasgow Road', col=BLUE, anchor='rm')
    e = S.img.px(dest(C, 108, rad+45)); S.label((e[0]+10, e[1]+30), '2  West High Street', col=MAGENTA, anchor='lm')
    S.render('b2-peel-park.jpg',
      head=dict(num='B2', title='PEEL PARK ROUNDABOUT', sub='A803 Glasgow Road, Kirkintilloch  ·  no lane markings', mph='30',
                route='YOUR ROUTE: FIRST EXIT, A803 Glasgow Road (it looks like straight on). Keep left. ◀ Signal left on approach and keep it on.'),
      legend=[LEG(BLUE, 'First exit  ·  YOUR ROUTE', 'Keep left. ◀ Signal left on approach, keep it on as you leave.', True),
              LEG(MAGENTA, 'Second exit, right: West High Street', 'Signal right ▶ on approach, keep right, ◀ signal left once past exit 1.', dash=True)],
      note='The 30 mph limit starts where Kirkintilloch Road becomes Glasgow Road, about 1 km before this roundabout.')
