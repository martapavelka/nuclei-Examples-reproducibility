#!/usr/bin/env python3
import json,sys
from itertools import combinations
p=sys.argv[1] if len(sys.argv)>1 else '../results/n00_collapse_certificate.json'
d=json.load(open(p)); facets=[tuple(x) for x in d['facets']]
C=set()
for F in facets:
 for r in range(1,len(F)+1): C.update(combinations(F,r))
for k,(s,t) in enumerate(d['collapse_pairs'],1):
 s=tuple(s);t=tuple(t)
 assert s in C and t in C, (k,'missing')
 assert len(t)==len(s)+1 and set(s)<set(t),(k,'not codim-one')
 co=[u for u in C if len(u)==len(t) and set(s)<set(u)]
 assert co==[t],(k,'not free',co)
 C.remove(s);C.remove(t)
remaining=sorted(C)
assert remaining==[tuple(d['remaining'][0])],remaining
print(f'VERIFIED: {len(d["collapse_pairs"])} elementary collapses; remaining vertex {remaining[0][0]}')
