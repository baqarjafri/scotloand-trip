# Bishopbriggs Test Route

Study guide for the Bishopbriggs driving test centre (Crosshill Road, B819, G64 2QA).
Open `index.html`. Each junction is one picture (`img/`): an aerial photo with the route lane,
lane arrows, other choices, traffic lights and signal points drawn on, plus the instruction and options.

## Cards

| Card | Junction | From Cadder |
|---|---|---|
| 0·1 | Gate → Cole Road roundabout (1st exit) | start |
| 2 | Retail park lights (straight on) | start |
| 3 | Lowmoss Roundabout (ahead = right lane) | start |
| 4 | Cadder Roundabout, A803 (A = 1st exit south, B = 2nd exit north) | 0 |
| A1 | Side road by Shell Lowmoss | 70 m |
| A2 | Westerhill Road lights (ahead = right lane) | 310 m |
| A3 | Meadowburn | 610 m |
| A4 | Asda + Hilton Road lights | 0.9–1.0 km |
| A5 | South Crosshill Road lights (30 mph) | 1.8 km |
| A6 | Bishopbriggs Cross (ahead = middle lane) | 2.1 km |
| A7 | Colston Road crossroads | 3.1 km |
| B1 | Torrance Roundabout (ahead = right lane) | 0.9 km |
| B2 | Peel Park Roundabout, Kirkintilloch (1st exit) | 3.9 km |
| B3 | New Lairdsland Road lights | 4.2 km |
| B4 | Milton Road lights | 4.5 km |

## Data and method

- Photos: Esri World Imagery (Maxar, Earthstar Geographics).
- Lanes (`turn:lanes`), exits, speed limits, geometry: OpenStreetMap via Nominatim, 17 Nov 2026.
- Exit order: bearing of each arm from the roundabout centre, counted clockwise.
- Signalling: Highway Code rules 184–190.
- `data/route-geometry.json` (start leg) and `data/extensions.json` (A and B centrelines, distances).

Lane arrows are volunteer-mapped and too small to verify in the photos. Check them with the Street View links.
Direction-sign wording is not included.
