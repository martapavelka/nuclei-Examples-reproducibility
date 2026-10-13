#!/usr/bin/env python3
"""Verify N00 facets, its designated plantri boundary, and exact manifold links."""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
import nucleus_lower_bound as nl

root = Path(__file__).resolve().parent.parent
survivors = json.loads((root / 'results/n00_facets.json').read_text())
assert len(survivors) == 1
record = survivors[0]
assert record['sphere'] == 689
facets = [tuple(face) for face in record['facets']]
assert len(facets) == len(set(facets)) == 35
assert sorted({v for f in facets for v in f}) == list(range(11))
lines = (root / 'data/boundaries_v11.asc').read_text().splitlines()
assert len(lines) == 1249
boundary = nl.sphere_faces(nl.parse_ascii(lines[record['sphere']]))

face_counts = Counter(face for tet in facets for face in combinations(tet, 3))
actual_boundary = {face for face, occurrences in face_counts.items() if occurrences == 1}
assert actual_boundary == set(boundary)
assert [len(nl.all_subfaces(facets, k)) for k in range(1, 5)] == [11, 54, 79, 35]
assert nl.betti_f2(facets) == [1, 0, 0, 0]
ok, message = nl.exact_check(facets, boundary, 11)
assert ok, message
print('VERIFIED: N00 has boundary #689, f = (11,54,79,35), all manifold links, and correct homology')
