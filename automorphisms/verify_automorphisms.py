#!/usr/bin/env python3
from itertools import combinations, permutations, product
from collections import Counter, defaultdict

FACETS = {
 frozenset(x) for x in [
(1,2,3,11),(1,2,8,11),(1,3,4,11),(1,4,5,11),(1,5,6,10),(1,5,10,11),
(1,6,7,10),(1,7,8,10),(1,8,10,11),(2,3,6,10),(2,3,6,11),(2,4,5,7),
(2,4,5,11),(2,4,6,10),(2,4,6,11),(2,4,7,9),(2,4,9,10),(2,5,7,8),
(2,5,8,11),(3,4,5,7),(3,4,7,11),(3,5,7,8),(3,5,8,9),(3,6,7,10),
(3,6,7,11),(3,7,8,10),(3,8,9,10),(4,6,8,9),(4,6,8,10),(4,6,9,11),
(4,7,9,11),(4,8,9,10),(5,6,8,9),(5,6,8,10),(5,8,10,11)]
}
V=sorted(set().union(*FACETS))

def faces(k):
    return {frozenset(c) for F in FACETS for c in combinations(F,k)}
E,T = faces(2), faces(3)
tri_deg=Counter(t for F in FACETS for t in map(frozenset, combinations(F,3)))
BT={t for t,d in tri_deg.items() if d==1}
BE={e for t in BT for e in combinations(t,2)}
BE={frozenset(e) for e in BE}

def signature(v):
    # All entries are combinatorial invariants, hence preserved by every automorphism.
    incident_tets=sum(v in F for F in FACETS)
    graph_deg=sum(v in e for e in E)
    boundary_deg=sum(v in e for e in BE)
    boundary_tri=sum(v in t for t in BT)
    interior_edge_deg_multiset=tuple(sorted(
        sum(e <= F for F in FACETS) for e in E if v in e and e not in BE
    ))
    return (incident_tets,graph_deg,boundary_deg,boundary_tri,interior_edge_deg_multiset)

classes=defaultdict(list)
for v in V: classes[signature(v)].append(v)
classes=list(classes.values())
print('Invariant vertex classes:', classes)
print('Candidate permutations after invariants:', end=' ')
ncand=1
for c in classes:
    import math; ncand*=math.factorial(len(c))
print(ncand)

def preserves_facets(p):
    return {frozenset(p[v] for v in F) for F in FACETS} == FACETS

autos=[]
for choices in product(*(list(permutations(c)) for c in classes)):
    p={}
    for c,img in zip(classes,choices): p.update(dict(zip(c,img)))
    if preserves_facets(p): autos.append(p)

print('Number of automorphisms:',len(autos))
for p in autos:
    print(' ', tuple(p[v] for v in V))

sigma={1:9,9:1,3:7,7:3,4:11,11:4,5:6,6:5,8:10,10:8,2:2}
assert preserves_facets(sigma)
assert len(autos)==2
assert any(all(p[v]==sigma[v] for v in V) for p in autos)
assert any(all(p[v]==v for v in V) for p in autos)
print('VERIFIED: Aut(N00) = {id, sigma} ~= Z/2Z')
