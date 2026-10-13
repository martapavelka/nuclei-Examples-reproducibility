#!/usr/bin/env python3
"""Exhaustively classify nuclei on 11 vertices, grouped by tetrahedron count."""
import argparse, json, sys, time
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix, vstack, csr_matrix
import nucleus_lower_bound as nl

def add_exact_t(model,t):
    row=lil_matrix((1,model['N']))
    row[0,:model['nx']]=1
    A=vstack([model['A'],csr_matrix(row)],format='csr')
    lo=np.r_[model['lo'],float(t)]; hi=np.r_[model['hi'],float(t)]
    return A,lo,hi

def enumerate_models(model,t):
    A,lo,hi=add_exact_t(model,t); blocks=[]
    while True:
        AA=vstack([A]+[b[0] for b in blocks],format='csr') if blocks else A
        LL=np.r_[lo, *([-np.inf]*len(blocks))]
        HH=list(hi)+[b[1] for b in blocks]
        r=milp(np.zeros(model['N']),integrality=np.ones(model['N']),
               bounds=Bounds(np.zeros(model['N']),np.ones(model['N'])),
               constraints=LinearConstraint(AA,LL,np.array(HH)),options={'presolve':True})
        if not r.success:
            if r.status==2: return
            raise RuntimeError(f'HiGHS status {r.status}: {r.message}')
        bits=np.rint(r.x[:model['nx']]).astype(int)
        if np.max(np.abs(r.x[:model['nx']]-bits))>1e-6:
            raise RuntimeError('nonintegral x solution')
        chosen=[model['tets'][i] for i,b in enumerate(bits) if b]
        yield chosen
        ones=np.flatnonzero(bits); zeros=np.flatnonzero(1-bits)
        ng=lil_matrix((1,model['N']))
        for i in ones: ng[0,i]=1
        for i in zeros: ng[0,i]=-1
        blocks.append((csr_matrix(ng),float(len(ones)-1)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--plantri',required=True)
    ap.add_argument('--out',default='v11_results.json')
    ap.add_argument('--t-min',type=int,default=14); ap.add_argument('--t-max',type=int,default=36)
    a=ap.parse_args()
    lines=nl.plantri_ascii(Path(a.plantri),11)
    if len(lines)!=1249: raise RuntimeError(f'expected 1249 boundary spheres, got {len(lines)}')
    result={'boundary_spheres':len(lines),'by_t':{},'survivors':[]}
    for t in range(a.t_min,a.t_max+1):
        feasible=0; rejected=Counter(); survivors=[]; start=time.time()
        for si,line in enumerate(lines):
            bfaces=nl.sphere_faces(nl.parse_ascii(line)); model=nl.build_model(11,bfaces)
            if model is None: continue
            for chosen in enumerate_models(model,t):
                feasible+=1
                ok,why=nl.exact_check(chosen,bfaces,11)
                if ok: survivors.append({'sphere':si,'facets':[list(x) for x in chosen]})
                else: rejected[why]+=1
        rec={'feasible_fillings':feasible,'rejections':dict(rejected),'survivors':survivors,'seconds':time.time()-start}
        result['by_t'][str(t)]=rec; result['survivors'].extend({'t':t,**x} for x in survivors)
        Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
        print(t,feasible,dict(rejected),'survivors',len(survivors),flush=True)
if __name__=='__main__': main()
