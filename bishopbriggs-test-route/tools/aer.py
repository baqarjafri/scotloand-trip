import json, math, os, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
TILES = os.path.join(HERE, 'aerial')
UA = 'route-study-script/1.0'
MPP19 = None
def tilexy(lon, lat, z):
    n = 2**z
    return (lon+180)/360*n, (1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
def fetch_box(lon0, lat0, lon1, lat1, z=19):
    xa, ya = tilexy(min(lon0, lon1), max(lat0, lat1), z); xb, yb = tilexy(max(lon0, lon1), min(lat0, lat1), z)
    x0, x1, y0, y1 = int(xa), int(xb), int(ya), int(yb)
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            f = f'{TILES}/{z}_{x}_{y}.jpg'
            if not os.path.exists(f) or os.path.getsize(f) < 100:
                subprocess.run(['curl', '-sS', '-m', '30', '-A', UA, '-o', f, f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'], check=True)
    im = Image.new('RGB', ((x1-x0+1)*256, (y1-y0+1)*256))
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            im.paste(Image.open(f'{TILES}/{z}_{x}_{y}.jpg').convert('RGB'), ((x-x0)*256, (y-y0)*256))
    return Img(im, z, x0, y0)
def font(sz, bold=True):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(f, int(sz))
class Img:
    def __init__(self, im, z, x0, y0):
        self.im, self.z, self.x0, self.y0 = im, z, x0, y0
        self.ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.ov)
        lat = None
    def px(self, p):
        X, Y = tilexy(p[0], p[1], self.z); return ((X-self.x0)*256, (Y-self.y0)*256)
    def mpp(self, lat): return 156543.03392*math.cos(math.radians(lat))/2**self.z
    def offset(self, pts, off_m):
        """offset polyline to the RIGHT of travel by off_m metres (negative = left)"""
        P = [self.px(p) for p in pts]; m = self.mpp(pts[0][1]); o = off_m/m; out = []
        for i, (x, y) in enumerate(P):
            a = P[max(i-1, 0)]; b = P[min(i+1, len(P)-1)]
            dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
            nx, ny = -dy/L, dx/L   # left normal in screen coords (y down): rotate (dx,dy) by -90 -> (dy,-dx) is right
            out.append((x - nx*o, y - ny*o))
        return out
    def ribbon(self, pts, off_m, width_m, rgba, arrow=True, outline=(255, 255, 255, 230)):
        P = self.offset(pts, off_m); w = max(2, width_m/self.mpp(pts[0][1]))
        self.d.line(P, fill=outline, width=int(w+6), joint='curve')
        self.d.line(P, fill=rgba, width=int(w), joint='curve')
        if arrow: self.head(P, rgba, w)
        return P
    def head(self, P, rgba, w):
        (x1, y1), (x2, y2) = P[-2], P[-1]; a = math.atan2(y2-y1, x2-x1); L = w*1.9; W = w*1.25
        tip = (x2+math.cos(a)*L, y2+math.sin(a)*L)
        l = (x2+math.sin(a)*W, y2-math.cos(a)*W); r = (x2-math.sin(a)*W, y2+math.cos(a)*W)
        self.d.polygon([tip, l, r], fill=rgba, outline=(255, 255, 255, 230))
    def line(self, pts, rgba, w=3, dash=None):
        P = [self.px(p) for p in pts]; self.d.line(P, fill=rgba, width=w)
    def finish(self):
        return Image.alpha_composite(self.im.convert('RGBA'), self.ov).convert('RGB')
