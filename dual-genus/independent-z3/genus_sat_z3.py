"""Exact orientable genus SAT test for facet-list dual graphs.

An orientable cellular embedding corresponds to a cyclic rotation at each
vertex. Labeling directed edges by facial cycles gives a finite SAT encoding.
An UNSAT result at genus g proves there is no genus <=g rotation system.
Requires Python 3 and libz3. The solver does not emit an UNSAT proof file.
"""
import ctypes,sys,itertools,time,re
import ctypes.util
from collections import defaultdict
from pathlib import Path

class SAT:
 def __init__(self):self.pool={};self.cls=[]
 def var(self,name):
  if name not in self.pool:self.pool[name]=len(self.pool)+1
  return self.pool[name]
 def clause(self,*xs):self.cls.append(tuple(xs))
 def atmostone(self,lits):
  if len(lits)<=7:
   for a,b in itertools.combinations(lits,2):self.clause(-a,-b)
  else:
   s=[self.var(('seq',len(self.pool),i)) for i in range(len(lits)-1)]
   self.clause(-lits[0],s[0]); self.clause(-lits[-1],-s[-1])
   for i in range(1,len(lits)-1):
    self.clause(-lits[i],s[i]);self.clause(-s[i-1],s[i]);self.clause(-lits[i],-s[i-1])
 def onehot(self,lits):self.clause(*lits);self.atmostone(lits)
 def solve(self,sec):
  library=ctypes.util.find_library('z3')
  if not library:
   try:
    from z3 import z3core
    library=str(Path(z3core.__file__).resolve().parent/'lib'/'libz3.so')
   except ImportError:
    raise RuntimeError('Z3 not found: install system libz3 or pip install z3-solver')
  z=ctypes.CDLL(library)
  z.Z3_mk_config.restype=ctypes.c_void_p
  z.Z3_mk_context.argtypes=[ctypes.c_void_p];z.Z3_mk_context.restype=ctypes.c_void_p
  z.Z3_mk_solver.argtypes=[ctypes.c_void_p];z.Z3_mk_solver.restype=ctypes.c_void_p
  z.Z3_solver_inc_ref.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
  z.Z3_solver_from_string.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
  z.Z3_solver_check.argtypes=[ctypes.c_void_p,ctypes.c_void_p];z.Z3_solver_check.restype=ctypes.c_int
  z.Z3_mk_params.argtypes=[ctypes.c_void_p];z.Z3_mk_params.restype=ctypes.c_void_p
  z.Z3_params_inc_ref.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
  z.Z3_params_set_uint.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint]
  z.Z3_mk_string_symbol.argtypes=[ctypes.c_void_p,ctypes.c_char_p];z.Z3_mk_string_symbol.restype=ctypes.c_void_p
  z.Z3_solver_set_params.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
  z.Z3_solver_get_reason_unknown.argtypes=[ctypes.c_void_p,ctypes.c_void_p];z.Z3_solver_get_reason_unknown.restype=ctypes.c_char_p
  t=time.time()
  defs=''.join('(declare-const x%d Bool)\n'%i for i in range(1,len(self.pool)+1))
  lines=[]
  for cl in self.cls:
   if len(cl)==1: body=('x%d'%cl[0]) if cl[0]>0 else '(not x%d)'%-cl[0]
   else:body='(or '+' '.join(('x%d'%a) if a>0 else '(not x%d)'%-a for a in cl)+')'
   lines.append('(assert '+body+')\n')
  formula=(defs+''.join(lines)).encode()
  print('formula size',len(formula), 'variables',len(self.pool),'clauses',len(self.cls),'time prepare',round(time.time()-t,1),flush=True)
  cfg=z.Z3_mk_config();c=z.Z3_mk_context(cfg);sol=z.Z3_mk_solver(c);z.Z3_solver_inc_ref(c,sol)
  par=z.Z3_mk_params(c);z.Z3_params_inc_ref(c,par)
  z.Z3_params_set_uint(c,par,z.Z3_mk_string_symbol(c,b'timeout'),int(sec*1000));z.Z3_solver_set_params(c,sol,par)
  print('sending to Z3',flush=True); t=time.time()
  z.Z3_solver_from_string(c,sol,formula)
  print('loaded Z3',round(time.time()-t,1),flush=True)
  k=z.Z3_solver_check(c,sol)
  print('Z3 answer',str(k),{-1:'UNSAT',0:'UNKNOWN',1:'SAT'}[k],'elapsed',round(time.time()-t,1),flush=True)
  if k==0:print('reason',z.Z3_solver_get_reason_unknown(c,sol),flush=True)
  return k

def build(name,target_genus):
 path=Path(__file__).resolve().parent/(name+'.txt')
 fs=[tuple(a for a in range(1,6) if a!=i) for i in range(1, 5 if name=='K4' else 6)] if name in ('K4','K5') else [tuple(map(int,re.findall(r'\d+',line))) for line in path.read_text().splitlines() if line.strip()]
 edgefaces=defaultdict(list)
 for i,f in enumerate(fs):
  for tri in itertools.combinations(f,3):edgefaces[tuple(sorted(tri))].append(i)
 neighbors=[set() for _ in fs]
 for incidence in edgefaces.values():
  if len(incidence)==2:
   v,u=incidence;neighbors[v].add(u);neighbors[u].add(v)
 n=len(fs);m=sum(map(len,neighbors))//2
 f=m-n+2-2*target_genus
 darts=sorted((u,v) for u,nb in enumerate(neighbors) for v in nb)
 ids={d:i for i,d in enumerate(darts)}
 N=len(darts)
 sat=SAT()
 # rotation options: first neighbor is fixed to erase local cyclic symmetry
 rotations={}
 for v,nb in enumerate(neighbors):
  ordered=sorted(nb)
  if len(ordered)<=2:rotations[v]=[(ordered,None)]
  else:
   opts=[]
   for k,tail in enumerate(itertools.permutations(ordered[1:])):
    choice=(ordered[0],)+tail
    lit=sat.var(('rot',v,k))
    opts.append((choice,lit))
   rotations[v]=opts
   sat.onehot([a[1] for a in opts])
 # face labels: darts have exactly one color; first occurrence order constraints
 for k in range(N):sat.onehot([sat.var(('x',k,i)) for i in range(min(f,k+1))])
 for k in range(N):
  for i in range(min(f,k+1)):
   mm=sat.var(('m',k,i));xx=sat.var(('x',k,i))
   if k==0 or i==k:
    sat.clause(-mm,xx)
   else:
    prev=sat.var(('m',k-1,i))
    sat.clause(-mm,xx,prev);sat.clause(-prev,mm)
   sat.clause(-xx,mm)
   if i>0:sat.clause(-xx,sat.var(('m',k-1,i-1)))
 sat.clause(sat.var(('m',N-1,f-1)))
 # rotation successor enforces identical face label on consecutive darts
 for d,(v,u) in enumerate(darts):
  for rot,lit in rotations[u]:
   k=rot.index(v);w=rot[(k+1)%len(rot)];d2=ids[(u,w)]
   limit1=min(f,d+1);limit2=min(f,d2+1)
   for color in range(max(limit1,limit2)):
    a=sat.var(('x',d,color)) if color<limit1 else None
    b=sat.var(('x',d2,color)) if color<limit2 else None
    if lit:
     if a and b:sat.clause(-lit,-a,b);sat.clause(-lit,-b,a)
     elif a:sat.clause(-lit,-a)
     elif b:sat.clause(-lit,-b)
    else:
     if a and b:sat.clause(-a,b);sat.clause(-b,a)
     elif a:sat.clause(-a)
     elif b:sat.clause(-b)
 print(name,'V',n,'E',m,'test genus <=',target_genus,'required faces',f,flush=True)
 return sat

if __name__=='__main__':
 name=sys.argv[1];g=int(sys.argv[2]);t=float(sys.argv[3]) if len(sys.argv)>3 else 60
 s=build(name,g)
 s.solve(t)
