#!/usr/bin/env python3
"""Pure standard-library input audit, not a knot classifier."""
import json,itertools,collections
from pathlib import Path
from verify_spanning_edges import spanning_edges
D=json.loads((Path(__file__).parent/'complexes.json').read_text())
for name in ('N0','N1'):
 K=[tuple(t) for t in D['complexes'][name]]
 assert len(K)==37 and len(set(map(tuple,map(sorted,K))))==37
 vertices=set().union(*map(set,K));assert len(vertices)==12
 faces={k:{tuple(sorted(x)) for t in K for x in itertools.combinations(t,k)} for k in (1,2,3,4)}
 counts=collections.Counter(tuple(sorted(x)) for t in K for x in itertools.combinations(t,3))
 boundary=[x for x,n in counts.items() if n==1]
 boundary_edges={tuple(sorted(e)) for t in boundary for e in itertools.combinations(t,2)}
 print(name,'f_vector=',tuple(len(faces[k]) for k in (1,2,3,4)),
       'boundary_triangles=',len(boundary),'boundary_edges=',len(boundary_edges),
       'spanning_edges=',len(spanning_edges(K)))
 assert tuple(len(faces[k]) for k in (1,2,3,4))==(12,58,84,37)
 assert len(boundary)==20 and len(boundary_edges)==30 and len(spanning_edges(K))==28
