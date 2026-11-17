import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *
W = load_ways(['osm/ways1.json', 'osm/ways2.json', 'osm/ways3.json'])
C = centre_low = (-4.2083686, 55.921989)
S = Scene((-4.20975, 55.92265, -4.20700, 55.92125))
app2 = W[1427552263]          # two-way, 1 lane each way
flare = W[1222830046]              # oneway, 2 lanes: left | through;right
exitSW = list(reversed(W[247132526]))
nw = W[31093561]
# paths (offset + = right of travel)
right_app = S.P([(app2, -1.7), (flare, +1.7)])
left_app = S.P([(app2, -1.7), (flare, -1.7)])
inner = lambda b0, b1: S.P([(arc(C, 6.4, b0, b1), 0)])
outer = lambda b0, b1: S.P([(arc(C, 9.6, b0, b1), 0)])
ahead = right_app + inner(80, 222) + S.P([([dest(C, 228, 15), exitSW[0]] + exitSW[1:], -1.7)])
left = left_app + outer(70, 122) + S.P([([dest(C, 125, 11), dest(C, 136, 34)], -1.6)])
right = right_app + inner(80, 282) + S.P([(nw, -1.6)])
S.path(left, MAGENTA, w=11, dash=22)
S.path(right, ORANGE, w=11, dash=22)
S.path(ahead, BLUE, w=15)
# lane labels on the approach
la = S.offpx(flare, -1.7)[0]; ra = S.offpx(flare, +1.7)[0]
S.label((la[0]-190, la[1]-60), 'LEFT LANE\nleft only', col=MAGENTA, sz=26, anchor='mm', dot=la)
S.label((ra[0]+150, ra[1]+40), 'RIGHT LANE\nahead or right', col=BLUE, sz=26, anchor='mm', dot=ra)
up = S.offpx(app2, -1.7)[1]
S.signal((up[0]-120, up[1]-110), 'N', text='NO SIGNAL on approach\n(going ahead)', anchor='mm')
# signal point after passing the 1st exit
sp = inner(155, 160)[0]
S.label((sp[0]+40, sp[1]+170), '◀ SIGNAL LEFT\nonce past exit 1', col=INK, bg=AMBER, border=INK, sz=26, anchor='mm', dot=sp)
# exit names
e1 = S.pt(dest(C, 136, 36)); S.label((e1[0]+30, e1[1]-10), '1  Retail park', col=MAGENTA, sz=26, anchor='lm')
e2 = ahead[-1]; S.label((e2[0]+10, e2[1]+60), '2  To Cadder Rbt (A803)', col=BLUE, sz=26, anchor='lm')
e3 = right[-1]; S.label((e3[0]+10, e3[1]-60), '3  Burger King', col=ORANGE, sz=26, anchor='lm')
S.render('j03-lowmoss.jpg',
  head=dict(num='3', title='LOWMOSS ROUNDABOUT', sub='B819 Crosshill Road  ·  4 exits  ·  ≈300 m after the lights', mph='40',
            route='YOUR ROUTE: AHEAD, 2nd exit. Get in the RIGHT lane. No signal on approach. ◀ Signal left once you pass the retail-park exit.'),
  legend=[dict(color=BLUE, told='Ahead (2nd exit)  ·  YOUR ROUTE', lane='RIGHT', **{'in': 'no signal', 'out': '◀ after exit 1'}, primary=True),
          dict(color=MAGENTA, told='First exit, left (retail park)', lane='LEFT', dash=True, **{'in': '◀ left', 'out': 'keep ◀ on'}),
          dict(color=ORANGE, told='Third exit, right (Burger King)', lane='RIGHT', dash=True, **{'in': 'right ▶', 'out': '◀ after exit 2'})],
  note='Trap: the left lane is LEFT ONLY. Sitting in it by habit takes you into the car park.')
