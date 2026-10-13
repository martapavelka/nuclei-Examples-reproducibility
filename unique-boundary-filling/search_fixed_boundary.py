import itertools as it, sys, time, json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack,csr_matrix
import nucleus_core as nl
ROOT=Path(__file__).resolve().parent
orig=[tuple(int(x)-1 for x in l.split()) for l in (ROOT/'N00_facets.txt').read_text().splitlines() if l.strip()]
tc=Counter(tuple(sorted(f)) for T in orig for f in it.combinations(T,3))
bf=sorted(f for f,c in tc.items() if c==1)
model=nl.build_model(11,bf)

def manifold_and_betti(ch):
    tets=[tuple(sorted(T)) for T in ch]; bfaces=set(bf)
    tc=Counter(tuple(sorted(f)) for T in tets for f in it.combinations(T,3))
    if {f for f,c in tc.items() if c==1}!=bfaces or any(c not in (1,2) for c in tc.values()): return None
    bedges=nl.all_subfaces(bfaces,2)
    for f,c in tc.items():
        if c==2 and sum(tuple(sorted(e)) in bedges for e in it.combinations(f,2))>1:return None
    owners=defaultdict(list)
    for i,T in enumerate(tets):
        for f in it.combinations(T,3): owners[tuple(sorted(f))].append(i)
    de=[tuple(v) for v in owners.values() if len(v)==2]
    if not nl.graph_connected(de,set(range(len(tets)))):return None
    for v in range(11):
        if not nl.check_disk_link(nl.link_complex(tets,(v,))):return None
    for e in nl.all_subfaces(tets,2):
        if not nl.check_1manifold_link(nl.link_complex(tets,e),e not in bedges):return None
    return nl.betti_f2(tets)

def enumerate_t(t):
    m=model; rr=lil_matrix((1,m['N']));rr[0,:m['nx']]=1
    A=vstack([m['A'],csr_matrix(rr)],format='csr');lo=np.r_[m['lo'],t];hi=np.r_[m['hi'],t]
    blocks=[]; raw=0; mans=[]
    while True:
        AA=vstack([A]+[b[0] for b in blocks],format='csr') if blocks else A
        LL=np.concatenate([lo]+[b[1] for b in blocks]) if blocks else lo
        HH=np.concatenate([hi]+[b[2] for b in blocks]) if blocks else hi
        r=milp(np.zeros(m['N']),integrality=np.ones(m['N']),bounds=Bounds(np.zeros(m['N']),np.ones(m['N'])),constraints=LinearConstraint(AA,LL,HH),options={'presolve':True})
        if not r.success:
            if r.status!=2: raise RuntimeError(r.message)
            break
        bits=np.rint(r.x[:m['nx']]).astype(int);ch=[m['tets'][i] for i,b in enumerate(bits) if b];raw+=1
        b=manifold_and_betti(ch)
        if b is not None: mans.append((b,ch))
        ones=np.flatnonzero(bits);zeros=np.flatnonzero(1-bits);ng=lil_matrix((1,m['N']))
        for i in ones:ng[0,i]=1
        for i in zeros:ng[0,i]=-1
        blocks.append((csr_matrix(ng),np.array([-np.inf]),np.array([len(ones)-1.])))
    return raw,mans

print('boundary triangles',len(bf),'boundary edges',len(nl.all_subfaces(bf,2)))
print('candidate tetrahedra',model['nx'])
out={}; ball=[]
for t in range(14,37):
    st=time.time();raw,mans=enumerate_t(t);hist=Counter(tuple(b) for b,_ in mans)
    print(t,'raw',raw,'manifold',len(mans),'betti',dict(hist),'sec',round(time.time()-st,2),flush=True)
    out[str(t)]={'raw_incidence_solutions':raw,'manifold_candidates':len(mans),'betti_histogram':{str(k):v for k,v in hist.items()}}
    for b,ch in mans:
        if b==[1,0,0,0]:ball.append((t,ch))
assert len(ball)==1, ball
assert set(ball[0][1])==set(orig), 'unique homology-ball survivor is not N00'
(ROOT/'results.json').write_text(json.dumps({'boundary_triangles':[[x+1 for x in f] for f in bf],'counts':out,'ball_homology_survivors':1,'survivor_is_N00':True},indent=2))
print('UNIQUE BALL-HOMOLOGY SURVIVOR = N00')
