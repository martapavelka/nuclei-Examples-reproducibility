"""Reconstruct the intrinsic stratification of three nuclei from facet lists.

No third-party Python libraries required. For Nmin, compare the full oriented
region attaching words with the Bing-house presentation in Fagan--Qiu--Wang
(2026, Sec. 3.3.2). For NCEY and NBL, compare the complexity-one spine type.
"""
import json
from collections import Counter, defaultdict, deque
from itertools import combinations, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPLEXES = json.loads((HERE / 'complexes.json').read_text())['complexes']

BING_BIG = (3, -1, -3, 2, -1, -2, -4, 2, -3, -4)
BING_SMALL = [(4,), (-1,)]

def normalize_facets(facets):
    return sorted(tuple(sorted(t)) for t in facets)

def cyclic_equal(a,b):
    return len(a)==len(b) and any(tuple(a[i:]+a[:i])==tuple(b) for i in range(len(a)))

def read_polyhedron(facets):
    N=normalize_facets(facets)
    tri=Counter(f for t in N for f in combinations(t,3))
    btri={f for f,c in tri.items() if c==1}
    bdry={e for f in btri for e in combinations(f,2)}
    interior={e for t in N for e in combinations(t,2) if e not in bdry}
    junctions={i for i,t in enumerate(N) if all(e in interior for e in combinations(t,2))}
    singular={f for f,c in tri.items() if c==2 and all(e in interior for e in combinations(f,2))}
    owners=defaultdict(list)
    for i,t in enumerate(N):
        for f in combinations(t,3):
            if f in singular: owners[f].append(i)
    G=defaultdict(list)
    for f in singular:
        i,j=owners[f];G[i].append((j,f));G[j].append((i,f))
    assert all(len(G[i])==(4 if i in junctions else 2) for i in G)
    paths=[];seen=set()
    for i in sorted(junctions):
        for j,f in sorted(G[i]):
            if f in seen:continue
            seen.add(f);nodes=[i,j];faces=[f]
            while nodes[-1] not in junctions:
                nxt=[(k,h) for k,h in G[nodes[-1]] if h not in seen]
                assert len(nxt)==1
                k,h=nxt[0];nodes.append(k);faces.append(h);seen.add(h)
            paths.append((nodes,faces))
    assert seen==singular
    # Regions are components of interior-edge dual polygons, joined across
    # regular dual edges (interior triangles with one boundary edge).
    parent={e:e for e in interior}
    def find(e):
        if parent[e]!=e:parent[e]=find(parent[e])
        return parent[e]
    def union(a,b):parent[find(a)]=find(b)
    for f,c in tri.items():
        if c!=2:continue
        inside=[e for e in combinations(f,2) if e in interior]
        assert len(inside) in (2,3)
        if len(inside)==2:union(*inside)
    regions=defaultdict(list)
    for e in sorted(interior):regions[find(e)].append(e)
    # Each polygon dual to an interior edge has a cyclic link. Choose an
    # orientation, then propagate face orientations over glued regular edges.
    cycle_edge={}
    for e in interior:
        incident=[i for i,t in enumerate(N) if set(e)<=set(t)]
        adj=defaultdict(list)
        for f,c in tri.items():
            if c!=2 or not set(e)<=set(f):continue
            isides=[i for i in incident if set(f)<=set(N[i])]
            assert len(isides)==2
            a,b=isides;adj[a].append((b,f));adj[b].append((a,f))
        assert all(len(adj[i])==2 for i in incident)
        start=min(incident);node=start;prev=None;steps=0
        while True:
            candidates=sorted((x,f) for x,f in adj[node] if x!=prev)
            assert len(candidates)==(2 if prev is None else 1)
            nx,f=candidates[0];cycle_edge[e,f]=(node,nx)
            steps+=1
            if nx==start:break
            prev,node=node,nx
            assert steps<=len(incident)
        assert steps==len(incident)
    orient={}
    for edges in regions.values():
        first=edges[0];orient[first]=1;todo=deque([first]);inreg=set(edges)
        while todo:
            e=todo.popleft()
            for f in tri:
                if tri[f]!=2 or not set(e)<=set(f):continue
                pair=[a for a in combinations(f,2) if a in interior]
                if len(pair)!=2:continue
                other=pair[0] if pair[1]==e else pair[1] if pair[0]==e else None
                if other is None:continue
                assert other in inreg
                a=1 if cycle_edge[e,f][0]<cycle_edge[e,f][1] else -1
                b=1 if cycle_edge[other,f][0]<cycle_edge[other,f][1] else -1
                new=-orient[e]*a*b
                if other in orient:assert orient[other]==new
                else:orient[other]=new;todo.append(other)
    polygons={};location={}
    for e in interior:
        pairs=[]
        for f,c in tri.items():
            if c==2 and set(e)<=set(f):
                a,b=cycle_edge[e,f]
                if orient[e]<0:a,b=b,a
                pairs.append((a,b,f))
        out={a:(a,b,f) for a,b,f in pairs}
        assert len(out)==len(pairs)
        seq=[];node=pairs[0][0];start=node
        while True:
            a,b,f=out[node];seq.append((a,b,f));node=b
            if node==start:break
            assert len(seq)<=len(pairs)
        assert len(seq)==len(pairs)
        polygons[e]=seq
        for k,(_,__,f) in enumerate(seq):location[e,f]=k
    face_path={}
    for path_id,(nodes,fs) in enumerate(paths,1):
        for k,f in enumerate(fs):face_path[f]=(path_id,(nodes[k],nodes[k+1]))
    def next_boundary(e,f):
        while True:
            f=polygons[e][(location[e,f]+1)%len(polygons[e])][2]
            if f in singular:return (e,f)
            other=[a for a in combinations(f,2) if a in interior and a!=e]
            assert len(other)==1
            e=other[0]
    words=[]
    for edges in regions.values():
        darts={(e,f) for e in edges for f in singular if set(e)<=set(f)}
        assert darts
        start=min(darts);d=start;w=[]
        while True:
            assert d in darts
            darts.remove(d)
            e,f=d;a,b,_=polygons[e][location[d]]
            p,(u,v)=face_path[f]
            assert (a,b) in ((u,v),(v,u))
            w.append(p if (a,b)==(u,v) else -p)
            d=next_boundary(e,f)
            if d==start:break
            assert len(w)<200
        assert not darts, 'non-disk region?'
        runs=[]
        for x in w:
            if not runs or runs[-1][0]!=x:runs.append([x,1])
            else:runs[-1][1]+=1
        if len(runs)>1 and runs[0][0]==runs[-1][0]:
            runs[0][1]+=runs[-1][1]
            runs.pop()
        compact=[]
        for x,count in runs:
            path_len=len(paths[abs(x)-1][1])
            assert count%path_len==0, (x,count,path_len)
            compact.extend([x]*(count//path_len))
        words.append(compact)
    return N,paths,regions,words

def matches_bing(paths,words):
    assert len(paths)==4 and len(words)==3
    loop=[i+1 for i,(p,f) in enumerate(paths) if p[0]==p[-1]]
    bridge=[i+1 for i,(p,f) in enumerate(paths) if p[0]!=p[-1]]
    assert len(loop)==2 and len(bridge)==2
    for lp in permutations((1,4)):
        for bp in permutations((2,3)):
            names=dict(zip(loop,lp))|dict(zip(bridge,bp))
            for signs in product((-1,1),repeat=4):
                mark={p:signs[p-1]*names[p] for p in range(1,5)}
                mapped=[[mark[abs(x)]*(1 if x>0 else -1) for x in w] for w in words]
                b=[w for w in mapped if len(w)==10]
                sm=[w for w in mapped if len(w)==1]
                if len(b)!=1 or len(sm)!=2:continue
                if sorted(map(lambda w:abs(w[0]),sm))!=[1,4]:continue
                if cyclic_equal(b[0],list(BING_BIG)):
                    return mark, b[0], sm
                reverse=[-x for x in reversed(b[0])]
                if cyclic_equal(reverse,list(BING_BIG)):
                    return mark,reverse,sm
    return None

def main():
    for label,pretty in [('N00','N_min'),('N0','N_CEY'),('N1','N_BL')]:
        N,paths,regions,words=read_polyhedron(COMPLEXES[label])
        loops=sum(p[0]==p[-1] for p,f in paths)
        print(pretty,'tetrahedra=',len(N),'intrinsic vertices=',len(set(i for p,_ in paths for i in (p[0],p[-1]))),'singular edges=',len(paths),'loops=',loops,'regions=',len(regions),'word lengths=',sorted(map(len,words)))
        if label=='N00':
            assert len(paths)==4 and loops==2 and len(regions)==3
            match=matches_bing(paths,words)
            assert match, 'Bing presentation did not match'
            print('  Bing house identification PASS; renaming of oriented intrinsic edges:',match[0])
            print('  long attaching word:',match[1])
            print('  small boundary words:',match[2])
        else:
            assert len(paths)==2 and loops==2 and len(regions)==2
            print('  complexity-one three-ball spine (the abalone): PASS')

if __name__=='__main__':main()
