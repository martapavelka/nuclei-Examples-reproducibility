#!/usr/bin/env python3
"""Independently replay every simplicial collapse, checking all cofaces."""
import json
import sys
from itertools import combinations
from pathlib import Path

source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('results/n00_collapse_certificate.json')
obj = json.loads(source.read_text())
facets = [tuple(f) for f in obj['facets']]
assert all(tuple(sorted(f)) == f and len(f) == 4 for f in facets)
assert len(facets) == len(set(facets))
canonical_path = Path(__file__).resolve().parent.parent / 'results/n00_facets.json'
if canonical_path.exists():
    expected_facets = {tuple(f) for f in json.loads(canonical_path.read_text())[0]['facets']}
    assert set(facets) == expected_facets, 'certificate facets differ from N00 facets'
complex_faces = {s for facet in facets for k in range(1, 5) for s in combinations(facet, k)}

for step, (small, large) in enumerate(obj['collapse_pairs'], 1):
    small, large = tuple(small), tuple(large)
    assert small in complex_faces and large in complex_faces, (step, 'face missing')
    assert len(large) == len(small) + 1 and set(small) < set(large), (step, 'wrong dimensions')
    proper_cofaces = [face for face in complex_faces
                      if len(face) > len(small) and set(small) < set(face)]
    assert proper_cofaces == [large], (step, 'not free', proper_cofaces)
    complex_faces.remove(small)
    complex_faces.remove(large)

expected_remaining = {tuple(vertex) for vertex in obj['remaining']}
assert complex_faces == expected_remaining and len(complex_faces) == 1, complex_faces
print(f'VERIFIED (all cofaces): {len(obj["collapse_pairs"])} elementary collapses to {next(iter(complex_faces))}')
