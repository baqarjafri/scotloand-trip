import math, os, subprocess, sys
from PIL import Image
UA = 'route-study-script/1.0 (personal driving-route study)'
def t(lon, lat, z):
    n = 2**z; return (lon+180)/360*n, (1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
def strip(pts, z, margin, out):
    tiles = set()
    for (la1, lo1), (la2, lo2) in zip(pts, pts[1:]):
        for i in range(41):
            la = la1+(la2-la1)*i/40; lo = lo1+(lo2-lo1)*i/40; x, y = t(lo, la, z)
            for dx in range(-margin, margin+1):
                for dy in range(-margin, margin+1): tiles.add((int(x)+dx, int(y)+dy))
    xs = [a for a, b in tiles]; ys = [b for a, b in tiles]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    im = Image.new('RGB', ((x1-x0+1)*256, (y1-y0+1)*256), (230, 230, 230))
    for (x, y) in tiles:
        f = f'tiles/{z}_{x}_{y}.png'
        if not os.path.exists(f): subprocess.run(['curl', '-sS', '-m', '30', '-A', UA, '-o', f, f'https://tile.openstreetmap.org/{z}/{x}/{y}.png'], check=True)
        im.paste(Image.open(f).convert('RGB'), ((x-x0)*256, (y-y0)*256))
    im.save(out); print(out, im.size, len(tiles), 'tiles', 'origin', z, x0, y0)
if __name__ == '__main__':
    z = int(sys.argv[1]); m = int(sys.argv[2]); out = sys.argv[3]
    pts = [tuple(map(float, p.split(','))) for p in sys.argv[4:]]
    strip(pts, z, m, out)
