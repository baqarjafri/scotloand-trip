# Bishopbriggs Test Route

Study guide for the Bishopbriggs driving test centre (Crosshill Road, B819, G64 2QA).
One card ("module") per junction, in driving order. Each card gives the lane, the signal on approach,
what to do on the roundabout, the signal to leave, the common mistake, the data source and a Street View link.

Open `index.html` in a browser.

## Status

| Card | Junction | Status |
|---|---|---|
| 0 | Test centre gate → Crosshill Road (turn left) | Sample, gate position to confirm |
| 1 | Cole Road roundabout (1st exit) | Sample |
| 2 | Retail park traffic lights (straight on) | Sample |
| 3 | Lowmoss Roundabout (ahead = right lane) | Sample, check arrows on Street View |
| 4 | Cadder Roundabout, A803 (fork: A = 1st exit south, B = 2nd exit north) | Sample, check arrows on Street View |
| A | A803 south past Asda and Morrisons, to ~4 miles | Waiting for route confirmation |
| B | A803 north via Torrance Roundabout, to ~4 miles | Waiting for route confirmation |

## Data and method

- Lanes, lane arrows (`turn:lanes`), exits and speed limits: OpenStreetMap tags, read through Nominatim
  (17 Nov 2026). Way IDs are printed on each card.
- Exit order: bearing of each arm from the roundabout centre, counted clockwise.
- Signalling: Highway Code rules 184–190.
- Maps in `img/`: © OpenStreetMap contributors, with the route drawn on top.
- `data/route-geometry.json`: the drawn route line and junction centres (lon, lat).

OpenStreetMap lane arrows are volunteer-mapped. Check each card against the Street View link before relying on it.
