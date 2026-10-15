import json, functools, time
from pathlib import Path
from itertools import combinations
complexes=json.loads((Path(__file__).parent / 'complexes.json').read_text())['complexes']

def maximal(fs):
 fs={f for f in fs if f}
 return tuple(sorted((f for f in fs if not any(f!=g and (f&g)==f for g in fs))))

for name in ['N00','N0','N1']:
 data=tuple(sorted(sum((1<<v for v in tet),0) for tet in complexes[name]))
 count=[0]; began=time.monotonic()
 @functools.lru_cache(maxsize=None)
 def f(fs):
  count[0]+=1
  if len(fs)<=1: return len(fs)==1 # simplex
  vs=0
  for facet in fs: vs|=facet
  for v in range(15):
   if not vs&(1<<v):continue
   link=maximal([w&~(1<<v) for w in fs if w&(1<<v)])
   if not link or not f(link): continue
   dele=maximal(w&~(1<<v) for w in fs)
   if f(dele): return True
  return False
 result=f(data)
 print(name, 'non-evasive=',result,'states',count[0],'seconds',round(time.monotonic()-began,3), 'memo', f.cache_info(),flush=True)
