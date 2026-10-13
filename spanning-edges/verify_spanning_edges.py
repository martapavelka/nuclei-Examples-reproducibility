#!/usr/bin/env python3
import argparse,collections,itertools,json,time
from pathlib import Path

def boundary_edges(K):
 c=collections.Counter(tuple(sorted(f)) for T in K for f in itertools.combinations(T,3))
 return {tuple(sorted(e)) for f,n in c.items() if n==1 for e in itertools.combinations(f,2)}
def spanning_edges(K):
 return sorted({tuple(sorted(e)) for T in K for e in itertools.combinations(T,2)}-boundary_edges(K))
def exterior_facets(K,e):
 forbidden={(e[0],),(e[1],),tuple(sorted(e))};fs=set()
 for T in K:
  for p in itertools.permutations(T):
   s=[];chain=[]
   for x in p:s.append(x);chain.append(tuple(sorted(s)))
   q=frozenset(v for v in chain if v not in forbidden)
   if q:fs.add(q)
 L=list(fs);return {f for f in L if not any(f<g for g in L)}
def collapse(M):
 M=set(M);pairs=0
 while True:
  own=collections.defaultdict(list)
  for t in M:
   if len(t)>=2:
    for v in t:own[t-{v}].append(t)
  ch=None
  for s,ls in own.items():
   if len(ls)==1:
    t=ls[0]
    if not any(s<=u for u in M if u!=t) and (ch is None or len(t)>len(ch[1])):ch=(s,t)
  if ch is None:break
  s,t=ch;M.remove(t)
  for q in [t-{v} for v in s]:
   if not any(q<=u for u in M):M={u for u in M if not u<q};M.add(q)
  pairs+=1
 V=set().union(*M) if M else set();E={frozenset(x) for f in M for x in itertools.combinations(f,2)}
 d=max((len(f)-1 for f in M),default=-1);A={v:set() for v in V}
 for e in E:a,b=tuple(e);A[a].add(b);A[b].add(a)
 seen=set();cc=0
 for v in V:
  if v not in seen:
   cc+=1;seen.add(v);st=[v]
   while st:
    z=st.pop()
    for w in A[z]:
     if w not in seen:seen.add(w);st.append(w)
 return {'collapse_pairs':pairs,'terminal_dim':d,'V':len(V),'E':len(E),'components':cc,'beta1':len(E)-len(V)+cc if d<=1 else None}
def run_edge(K,e):
 z=time.time();r=collapse(exterior_facets(K,e));r['edge']=list(e);r['seconds']=round(time.time()-z,3);r['pass']=r['terminal_dim']==1 and r['components']==1 and r['beta1']==1;return r

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--complex',dest='names',action='append',help='complex name; repeatable')
 p.add_argument('--all-edges',action='store_true',help='test all spanning edges instead of only the new edge of M1--M9')
 p.add_argument('--output',default='results.json')
 a=p.parse_args();here=Path(__file__).resolve().parent;D=json.loads((here/'complexes.json').read_text());Cs={k:[tuple(t) for t in v] for k,v in D['complexes'].items()}
 names=a.names or (list(Cs) if a.all_edges else [f'M{i}' for i in range(1,10)])
 out={'criterion':'terminal_dim=1, components=1, beta1=1','mode':'all spanning edges' if a.all_edges else 'new edge only','complexes':{}}
 for name in names:
  K=Cs[name]
  if a.all_edges: es=spanning_edges(K)
  else:
   if name=='N00': raise SystemExit('N00 has no construction new edge; use --all-edges for N00')
   es=[tuple(D['metadata'][name]['new_spanning_edge'])]
  rows=[];print(name,len(es),'edge(s)',flush=True)
  for i,e in enumerate(es,1):
   r=run_edge(K,e);rows.append(r);print(i,e,r,flush=True)
  out['complexes'][name]={'tetrahedra':len(K),'tested_edges':len(es),'all_pass':all(r['pass'] for r in rows),'results':rows}
  Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
