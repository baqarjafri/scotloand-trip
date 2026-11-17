import json, subprocess, time, sys, urllib.parse
UA = 'route-study-script/1.0'
def get(url, tries=6):
    for i in range(tries):
        r = subprocess.run(['curl', '-sS', '-m', '60', '-A', UA, url], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout); time.sleep(2.2); return d
        except Exception:
            time.sleep(10 * (i + 1))
    raise SystemExit('failed ' + url)
def search(q, vb, extra='&dedupe=0&limit=40&extratags=1&namedetails=1&polygon_geojson=1'):
    return get(f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&viewbox={vb}&bounded=1&format=json{extra}')
def reverse(lat, lon, zoom=17):
    return get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&zoom={zoom}&format=json&extratags=1&namedetails=1')
def lookup(ids):
    out = []
    for i in range(0, len(ids), 40):
        out += get('https://nominatim.openstreetmap.org/lookup?osm_ids=' + ','.join(ids[i:i+40]) + '&format=json&extratags=1&namedetails=1&polygon_geojson=1')
    return out
