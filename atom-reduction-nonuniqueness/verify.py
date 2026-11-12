"""Independent audit of Younan lemma counterexample, with elementary certificates.
Does not import the original script. Input is Table 1 of Durhuus-Pavelka.
"""
import re
from itertools import combinations
from collections import Counter,defaultdict
import networkx as nx
# Facets from Table 1 (the vertex-minimal 11-vertex nucleus).
facets=[frozenset(q) for q in [
    (1, 2, 3, 11),
    (1, 7, 8, 10),
    (2, 4, 6, 11),
    (3, 5, 7, 8),
    (4, 6, 8, 10),
    (1, 2, 8, 11),
    (1, 8, 10, 11),
    (2, 4, 7, 9),
    (3, 5, 8, 9),
    (4, 6, 9, 11),
    (1, 3, 4, 11),
    (2, 3, 6, 10),
    (2, 4, 9, 10),
    (3, 6, 7, 10),
    (4, 7, 9, 11),
    (1, 4, 5, 11),
    (2, 3, 6, 11),
    (2, 5, 7, 8),
    (3, 6, 7, 11),
    (4, 8, 9, 10),
    (1, 5, 6, 10),
    (2, 4, 5, 7),
    (2, 5, 8, 11),
    (3, 7, 8, 10),
    (5, 6, 8, 9),
    (1, 5, 10, 11),
    (2, 4, 5, 11),
    (3, 4, 5, 7),
    (3, 8, 9, 10),
    (5, 6, 8, 10),
    (1, 6, 7, 10),
    (2, 4, 6, 10),
    (3, 4, 7, 11),
    (4, 6, 8, 9),
    (5, 8, 10, 11),
]]

def face_lattice(tets):
    return {frozenset(c) for t in tets for k in range(5) for c in combinations(t,k)}

def chain(tets, n):
    return [frozenset(c) for t in tets for c in combinations(t,n+1)]

def bfaces(tets):
    counts=Counter(chain(tets,2))
    assert max(counts.values())<=2
    return list(f for f,n in counts.items() if n==1)

def subcomplex(facets):
    return {frozenset(c) for t in facets for k in range(len(t)+1) for c in combinations(t,k)}

def link(faces, f):
    return {s-f for s in faces if f <= s}

def triangulated_surface(tets, want_disc):
    """Test as combinatorial 2-manifold, connected and with right Euler characteristic."""
    tris=list(tets)
    assert all(len(t)==3 for t in tris)
    counter=Counter(e for t in tris for e in (frozenset(q) for q in combinations(t,2)))
    assert all(1<=c<=2 for c in counter.values())
    vertices=set().union(*tris)
    for v in vertices:
        nbr=Counter()
        vlink=[]
        for tr in tris:
            if v in tr:
                ee=tr-{v};assert len(ee)==2
                vlink.append(ee)
        edge_c=Counter()
        adj=defaultdict(set)
        for e in vlink:
            a,b=list(e);edge_c[a]+=1;edge_c[b]+=1
            adj[a].add(b);adj[b].add(a)
        assert set(edge_c.values()) <= {1,2}
        assert sum(d==1 for d in edge_c.values()) in (0,2)
        todo=[next(iter(edge_c))];seen=set()
        while todo:
            vv=todo.pop()
            if vv not in seen:
                seen.add(vv);todo.extend(adj[vv]-seen)
        assert seen == set(edge_c),('pinched vertex',v)
    chi=len(vertices)-len(counter)+len(tris)
    bd=[e for e,m in counter.items() if m==1]
    if want_disc:
        assert chi==1 and bd
        deg=Counter(v for e in bd for v in e)
        assert all(n==2 for n in deg.values())
    else:
        assert chi==2 and not bd
    # Connected 2-dimensional manifold: all triangles meet through edges.
    graph=nx.Graph()
    graph.add_nodes_from(range(len(tris)))
    inc=defaultdict(list)
    for i,tr in enumerate(tris):
        for e in combinations(tr,2): inc[frozenset(e)].append(i)
    for idx in inc.values():
        if len(idx)==2: graph.add_edge(*idx)
    assert nx.is_connected(graph)
    assert nx.check_planarity(graph)[0]
    return (len(vertices),len(counter),len(tris),chi,len(bd))

def verify_3ball(tets, label):
    assert len(tets)==len(set(tets)) and all(len(t)==4 for t in tets)
    bd=bfaces(tets)
    bs=triangulated_surface(bd,False)
    verts=set().union(*tets)
    bdv=set().union(*bd)
    assert verts == bdv
    for v in verts:
        vtri=[q-{v} for q in tets if v in q]
        triangulated_surface(vtri,True)
    # Connected tetrahedron dual graph and nucleus condition.
    dual=nx.Graph()
    dual.add_nodes_from(range(len(tets)))
    facet_tris=defaultdict(list)
    for i,t in enumerate(tets):
        for tri in combinations(t,3): facet_tris[frozenset(tri)].append(i)
    for ids in facet_tris.values():
        if len(ids)==2:dual.add_edge(*ids)
    assert nx.is_connected(dual)
    be={frozenset(e) for tr in bd for e in combinations(tr,2)}
    for tri, ids in facet_tris.items():
        if len(ids)==2:assert sum(frozenset(e) in be for e in combinations(tri,2))<=1
    return len(verts),len(tets),bs

def full_link_candidates(tets):
    F=face_lattice(tets)
    be={frozenset(e) for tr in bfaces(tets) for e in combinations(tr,2)}
    result=[]
    for edge in be:
        u,v=map(lambda k:frozenset((k,)),edge)
        if link(F,u)&link(F,v) == link(F,edge):result.append(tuple(sorted(edge)))
    return sorted(result)

def full_quotient(tets,edge,survivor):
    u,v=edge
    dead = v if survivor==u else u
    def mapping(s):return frozenset(survivor if x==dead else x for x in s)
    original=face_lattice(tets)
    mapped={mapping(s) for s in original}
    result=[mapping(t) for t in tets if len(mapping(t))==4]
    assert len(result)==len(set(result))
    assert mapped==face_lattice(result),('hanging faces',len(mapped-face_lattice(result)))
    return result

N=facets
print('Source Table 1:',len(N),'tetrahedra')
assert frozenset((1,2,3)) in bfaces(N)
M=[frozenset(i if i<4 else i+8 for i in t) for t in N]
shared=frozenset((1,2,3))
L=next(t for t in N if shared<=t)
R=next(t for t in M if shared<=t)
x=next(iter(L-shared));y=next(iter(R-shared))
G=[t for t in N+M if t not in (L,R)]
G += [frozenset((x,y,*e)) for e in combinations(shared,2)]
print('G:',verify_3ball(G,'G'),'atom?',not full_link_candidates(G))
H=[]
for tet in G:
    if {1,2}<=tet:
        H.extend([frozenset((k,20,*tuple(tet-{1,2}))) for k in (1,2)])
    else:H.append(tet)
print('H:',verify_3ball(H,'H'),'contractible edges:',full_link_candidates(H))
for e in [(1,20),(2,20),(8,20),(16,20)]:
    F=face_lattice(H)
    u,v=(frozenset([a]) for a in e)
    assert link(F,u)&link(F,v) == link(F,frozenset(e))
    qq=full_quotient(H,e,e[0]);report=verify_3ball(qq,str(e))
    remain=full_link_candidates(qq)
    # Edge link is an interval between boundary triangles
    EL=link(F,frozenset(e))
    nodes=sorted(next(iter(t)) for t in EL if len(t)==1)
    ellinks=sorted([tuple(sorted(t)) for t in EL if len(t)==2]); lg=nx.Graph(ellinks)
    assert nx.is_tree(lg) and len([n for n,d in lg.degree if d==1])==2
    assert set(nodes)==set(lg)
    print('CONTRACTION',e,'link path:',nx.shortest_path(lg,*[n for n,d in lg.degree if d==1]),'result:',report,'remaining valid contractions:',remain)
    if e==(1,20):
        print('returns G exactly?',set(qq)==set(G))
    if e==(8,20):
        K=qq
        print('K atom?',not remain)
print('Final checks: full simplicial quotient; vertex links; 2-sphere boundary; edge links; nucleus conditions all passed')
print('THESIS LEMMA 4.1.4 COUNTEREXAMPLE VERIFIED')
