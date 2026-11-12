#!/usr/bin/env python3
"""Verify the nine 12-vertex extensions and certify pairwise non-isomorphism.

Uses only the Python standard library and the published 1-based facet lists.
A vertex or edge degree is the number of tetrahedra containing it.
"""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "spanning-edges" / "complexes.json"
EXPECTED = Path(__file__).with_name("nine_extensions_invariants.json")
SIGMA = {1: 9, 2: 2, 3: 7, 4: 11, 5: 6, 6: 5,
         7: 3, 8: 10, 9: 1, 10: 8, 11: 4}


def facets(raw):
    result = {frozenset(t) for t in raw}
    assert len(result) == len(raw) and all(len(t) == 4 for t in result)
    return result


def boundary_triangles(tetrahedra):
    counts = Counter(frozenset(t) for f in tetrahedra for t in combinations(f, 3))
    assert all(deg in (1, 2) for deg in counts.values())
    return {t for t, deg in counts.items() if deg == 1}


def orbit(face):
    return frozenset((face, frozenset(SIGMA[v] for v in face)))


def invariant(tetrahedra):
    # These histograms are preserved by every simplicial isomorphism.
    vertex_degree = Counter(v for t in tetrahedra for v in t)
    edge_degree = Counter(frozenset(e) for t in tetrahedra for e in combinations(t, 2))
    return {
        "vertex_tetrahedron_degrees": {
            str(degree): count for degree, count in sorted(Counter(vertex_degree.values()).items())
        },
        "edge_tetrahedron_degrees": {
            str(degree): count for degree, count in sorted(Counter(edge_degree.values()).items())
        },
    }


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert data["vertex_labels"] == "1-based"
    base = facets(data["complexes"]["N00"])
    assert len(base) == 35 and set().union(*base) == set(range(1, 12))
    assert {frozenset(SIGMA[v] for v in f) for f in base} == base
    assert all(SIGMA[SIGMA[v]] == v for v in SIGMA)

    boundary = boundary_triangles(base)
    assert len(boundary) == 18
    boundary_orbits = {orbit(t) for t in boundary}
    assert len(boundary_orbits) == 9
    assert all(len(o) == 2 for o in boundary_orbits)
    assert set().union(*boundary_orbits) == boundary

    names = [f"M{i}" for i in range(1, 10)]
    assert set(data["metadata"]) == set(names)
    assert set(data["complexes"]) == {"N00", *names}
    representatives = []
    results = {}
    for name in names:
        meta = data["metadata"][name]
        face = frozenset(meta["construction_face"])
        removed = frozenset(meta["removed_tetrahedron"])
        x = meta["opposite_vertex"]
        assert face in boundary and removed in base
        assert len(face) == 3 and removed == face | {x}
        assert sorted(meta["new_spanning_edge"]) == sorted((x, 12))
        a, b, c = sorted(face)
        new = {
            frozenset((a, b, x, 12)),
            frozenset((a, c, x, 12)),
            frozenset((b, c, x, 12)),
        }
        expected_facets = (base - {removed}) | new
        actual = facets(data["complexes"][name])
        assert actual == expected_facets, f"Construction mismatch: {name}"
        assert len(actual) == 37 and set().union(*actual) == set(range(1, 13))
        representatives.append(orbit(face))
        results[name] = {
            "construction_face": sorted(face),
            **invariant(actual),
        }

    assert len(set(representatives)) == 9
    assert set(representatives) == boundary_orbits
    signatures = [
        (tuple(sorted(r["vertex_tetrahedron_degrees"].items())),
         tuple(sorted(r["edge_tetrahedron_degrees"].items())))
        for r in results.values()
    ]
    assert len(set(signatures)) == 9, "A pair of degree invariants coincides"
    assert json.loads(EXPECTED.read_text(encoding="utf-8")) == results, "Recorded invariants mismatch"

    print("PASS: 18 boundary triangles form 9 orbits under the stated involution")
    print("PASS: M1,...,M9 are exactly the nine recorded tetrahedron attachments")
    print("PASS: all 9 combined vertex/edge degree profiles are distinct")
    print("VERIFIED: the nine extensions are pairwise non-isomorphic")


if __name__ == "__main__":
    main()
