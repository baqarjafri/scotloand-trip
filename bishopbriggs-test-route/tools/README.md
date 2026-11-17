# Picture generator

Scripts that drew the junction pictures. `osm/` holds the OpenStreetMap ways they read.

- `compose.py`: picture layout (header, photo overlay, legend) and lane-from-tags helpers.
- `aer.py`: fetches and stitches Esri aerial tiles (cached in `aerial/`).
- `junctions.py`: one block per junction; run `python3 junctions.py a2 b1` to redraw only those.
- `j_lowmoss.py`: Lowmoss Roundabout. `overview2.py`: the full-route map and distances.
- `nom.py`: rate-limited Nominatim lookups. `strip.py`: street-map strips used to find junctions.
- `svgscene.py`: vector version of the scene. `MODE=svg python3 junctions.py` writes `../diag/*.json` (diagram SVG, lanes, legend).
- `build_page.py`: builds `../index.html` from `page_template.html` and `../diag/`, adding the driver's-eye lane view for each card.

Output paths are absolute (`OUTDIR` in `compose.py`); change them if you run this elsewhere.
