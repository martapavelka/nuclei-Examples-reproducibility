#!/usr/bin/env python3
"""Deterministic fundamental-group and Alexander certificates for two spanning edges.
Requires Python 3 and sympy for the polynomial gcd. The group reduction uses stdlib.
"""
import collections, itertools, json
from pathlib import Path
import sympy as sp

CASES={'N0': (9,11), 'N1':(2,3)}

def free_reduce(word):
    stack=[]
    for x in word:
        if stack and stack[-1]==-x: stack.pop()
        else: stack.append(x)
    while len(stack)>1 and stack[0]==-stack[-1]:stack=stack[1:-1]
    return tuple(stack)

def invert(word): return tuple(-x for x in reversed(word))

def presentation(K, edge):
    V=sorted(set().union(*map(set,K))-set(edge))
    faces={d: sorted({tuple(sorted(s)) for tet in K for s in itertools.combinations(set(tet)-set(edge), d)}) for d in (2,3)}
    parent={v:v for v in V}
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    tree=[]
    for a,b in faces[2]:
        ra,rb=root(a),root(b)
        if ra!=rb:parent[ra]=rb;tree.append((a,b))
    gens={edge:i+1 for i,edge in enumerate(e for e in faces[2] if e not in tree)}
    rels=[]
    for a,b,c in faces[3]:
        w=[]
        for u,v in [(a,b),(b,c),(c,a)]:
            if tuple(sorted((u,v))) in gens:
                w.append(gens[tuple(sorted((u,v)))]*(1 if u<v else -1))
        if w:rels.append(free_reduce(w))
    before=len(rels);steps=[]
    while True:
        candidate=None
        for j,w in enumerate(rels):
            for g,n in collections.Counter(map(abs,w)).items():
                if n==1:
                    p=next(i for i,x in enumerate(w) if abs(x)==g)
                    a,b=w[:p],w[p+1:]
                    replacement=free_reduce(invert(b)+invert(a) if w[p]>0 else b+a)
                    candidate=(j,g,replacement);break
            if candidate:break
        if candidate is None:break
        j,g,replacement=candidate
        oldrel=rels.pop(j)
        steps.append({'eliminated_generator':g,'using_relator':list(oldrel),'replacement':list(replacement)})
        rels=[free_reduce(tuple(y for x in w for y in (replacement if x==g else invert(replacement) if x==-g else (x,)))) for w in rels]
        rels=[w for w in rels if w]
    return {'remaining_relators':[list(r) for r in rels], 'remaining_generators':sorted(set(map(abs, itertools.chain.from_iterable(rels)))), 'initial_generators':len(gens), 'initial_relators':before, 'vertex_count':len(V), 'edge_count':len(faces[2]),'triangle_count':len(faces[3]), 'tree_edges':[list(e) for e in tree], 'generators':{str(v):list(e) for e,v in gens.items()},'tietze_eliminations':steps}

def alexander(rel, weights):
    t=sp.symbols('t'); prefix=0; derivatives={g:0 for g in weights}
    for letter in rel:
        g=abs(letter);v=weights[g]
        if letter>0: derivatives[g]+=t**prefix;prefix+=v
        else:prefix-=v;derivatives[g]-=t**prefix
    assert prefix==0
    poly=[]
    for f in derivatives.values():
        terms=sp.expand(f).as_ordered_terms()
        least=min(int(m.as_powers_dict().get(t,0)) for m in terms)
        poly.append(sp.Poly(sp.expand(f*t**(-least)),t))
    g=sp.gcd(*poly).monic()
    return {'abelianization_weights':{str(k):v for k,v in weights.items()},'fox_derivatives':{str(k):str(sp.expand(v)) for k,v in derivatives.items()},'alexander_polynomial':str(g.as_expr()), 'determinant':abs(int(g.eval(-1)))}

def main():
    complexes=json.loads((Path(__file__).parent/'complexes.json').read_text())['complexes'];out={}
    for name,edge in CASES.items():
        K=complexes[name];pres=presentation(K,edge);rels=pres['remaining_relators'];assert len(rels)==1
        r=rels[0]
        # Verify normalized two-generator torus-knot presentation.
        if name=='N0':
            assert r==[28,28,10,10,28],r
            # Cyclic conjugation gives x^3 y^2=1, x=g28, y=g10.
            weights={28:2,10:-3}
            normal='cyclically conjugate to x^3 y^2 (x=g28, y=g10)'
        else:
            assert r==[22,16,-22,16,-22,16],r
            # With x=g31 and u=x^-1*g25, the relator is x^2 u^3.
            weights={22:3,16:1}
            normal='substitution u=x^-1*y changes x*y*x^-1*y*x^-1*y into x^2*u^3 (x=g22, y=g16)'
        alex=alexander(r,weights)
        assert alex['alexander_polynomial']=='t**2 - t + 1',alex
        out[name]={'edge':list(edge),'verified_trefoil':True,'presentation':pres,'normal_form':normal,'alexander':alex}
        print(name,edge,'generators',pres['initial_generators'],'Tietze steps',len(pres['tietze_eliminations']),'relator',r,'Alexander',alex['alexander_polynomial'])
    (Path(__file__).parent/'trefoil_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
