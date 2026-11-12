"""Check all packaged facet lists and all atom non-contraction witnesses."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import contextlib
import io
import runpy

p = Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    data = runpy.run_path(str(p / "verify.py"))

def facets(name):
    rows = []
    for line in (p / f"{name}_facets.txt").read_text().splitlines():
        if line.strip():
            row = tuple(map(int,line.split()))
            assert len(row)==4 and len(set(row))==4 and row==tuple(sorted(row))
            rows.append(frozenset(row))
    assert len(rows)==len(set(rows))
    return set(rows)

for name in ("Nmin", "G", "H", "K"):
    obj = "N" if name=="Nmin" else name
    assert facets(name) == set(data[obj]), f"facet mismatch in {name}_facets.txt"
    print(f"{name}: {len(data[obj])} tetrahedra: exact facet list verified")

for name in ("G", "K"):
    tetrahedra = facets(name)
    bd = data["bfaces"](tetrahedra)
    b_edges = {frozenset(e) for t in bd for e in combinations(t,2)}
    ed = {frozenset(e) for t in tetrahedra for e in combinations(t,2)}
    tr = {frozenset(t) for q in tetrahedra for t in combinations(q,3)}
    txt=(p/"atom_witnesses.txt").read_text()
    section=txt.split(name+": 51 boundary edges",1)
    assert len(section)==2, f"Missing section {name}"
    remainder=section[1].split("\n\n",1)[0]
    parsed={}
    for row in remainder.splitlines():
        if not row.strip():continue
        left,right=row.split(":")
        a,b=map(int,left.split());c=int(right.strip())
        e=frozenset((a,b))
        assert e in b_edges and e not in parsed
        assert frozenset((a,c)) in ed and frozenset((b,c)) in ed
        assert frozenset((a,b,c)) not in tr
        parsed[e]=c
    assert set(parsed)==b_edges, f"Missing witnesses for {name}: {len(b_edges-set(parsed))}"
    assert len(parsed)==51
    print(f"{name}: complete, valid atomicity witnesses for all 51 boundary edges")

print("All facet files and atom certificates match the verified construction.")
