#!/usr/bin/env python3
"""Independently check explicit orientable embeddings. Python standard library only."""
import collections,itertools,json,re
from pathlib import Path
B=Path(__file__).resolve().parent
EXPECTED={'N00':(35,61,22,3),'N0':(37,64,23,3),'N1':(37,64,21,4)}
for name,(nv,ne,nf,ng) in EXPECTED.items():
    facets=[tuple(map(int,re.findall(r'\d+',line))) for line in (B/f'{name}.txt').read_text().splitlines() if line.strip()]
    meta=json.loads((B/f'{name}_genus_embedding.json').read_text())
    assert [list(f) for f in facets]==meta['facets'],f'facet source mismatch for {name}'
    assert len(facets)==nv
    incidence=collections.defaultdict(list)
    for i,fac in enumerate(facets,1):
        for tri in itertools.combinations(sorted(fac),3):incidence[tri].append(i)
    assert max(map(len,incidence.values()))<=2
    edge_set={tuple(sorted(s)) for s in incidence.values() if len(s)==2}
    assert len(edge_set)==ne
    nbr={i:set() for i in range(1,nv+1)}
    for a,b in edge_set:nbr[a].add(b);nbr[b].add(a)
    rot={int(i):list(vs) for i,vs in meta['rotation'].items()}
    assert set(rot)==set(nbr)
    assert all(len(rot[i])==len(nbr[i]) and set(rot[i])==nbr[i] for i in nbr)
    darts={(v,u) for v in nbr for u in nbr[v]}
    visited=set();cycles=[]
    for d in sorted(darts):
        if d in visited:continue
        cur=d;face=[]
        while cur not in visited:
            assert cur in darts
            visited.add(cur);face.append(cur)
            v,u=cur;lst=rot[u];cur=(u,lst[(lst.index(v)+1)%len(lst)])
        assert cur==d,'face failed to close on starting dart'
        cycles.append(face)
    assert visited==darts
    F=len(cycles);chi=nv-ne+F
    assert (2-chi)%2==0
    g=(2-chi)//2
    assert (nv,ne,F,g)==(nv,ne,nf,ng)
    assert meta['genus']==ng and meta['faces']==nf
    if 'face_cycles' in meta:assert len(meta['face_cycles'])==F
    print(f'{name}: {nv} vertices, {ne} edges, {F} facial cycles, Euler characteristic {chi}, genus {g}: VERIFIED')
