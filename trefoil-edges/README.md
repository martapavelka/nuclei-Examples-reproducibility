# Trefoil certificates for two 12-vertex nuclei

The paper denotes `N0` by $N_{\mathrm{CEY}}$ and `N1` by
$N_{\mathrm{BL}}$. The certified knotted spanning edges are $[9,11]$
and $[2,3]$, respectively. All facet lists use 1-based labels.

## Reproduce the result

Install SymPy and run:

```bash
python3 verify_inputs.py
python3 certify_trefoil_edges.py
```

`verify_inputs.py` verifies the stored complexes, and
`certify_trefoil_edges.py` reconstructs the trefoil group and Alexander
polynomial certificates saved in `trefoil_certificates.json`.
The additional spanning-edge data and verifier are self-contained copies
of the corresponding computations in `spanning-edges/`.

## Trefoil spanning edges in N0 and N1

Run `python3 certify_trefoil_edges.py` (requires SymPy) to reproduce
`trefoil_certificates.json`. The full subcomplex obtained by deleting both
endpoints of a spanning edge is a deformation retract of the exterior of a
regular neighborhood of that edge (the simplicial complement/derived
neighborhood theorem). Accordingly its two-skeleton presents the knot group.

For **N0**, the edge is `[9,11]`. A spanning tree of the deleted-vertices
subcomplex gives 29 generators; elementary Tietze eliminations leave
`<x,y | x*x*y*y*x>` (the script's x=g28, y=g10). This relator is cyclically
conjugate to `x^3*y^2`, the (2,3) torus-knot group.

For **N1**, the edge is `[2,3]`. Starting with 28 generators, eliminations
leave `<x,y | x*y*x^-1*y*x^-1*y>` (x=g22, y=g16). Setting `u=x^-1*y`
transforms the relator into `x^2*u^3`, again the (2,3) torus-knot group.

The script also computes the Alexander polynomial from the Fox derivatives
of each resulting two-generator, one-relator presentation. In both cases it
is `t^2-t+1` (up to multiplication by a unit `±t^k`), hence determinant 3.
The nonabelian knot groups have nontrivial center; the theorem characterizing
knots with nontrivial central element as torus knots then identifies both
edges as trefoil-knotted spanning arcs (unoriented, so mirror chirality is
not determined). The Alexander polynomial *alone* would not identify a
specific knot type.

`trefoil_certificates.json` records the original graph generators and spanning
tree, every Tietze elimination (eliminated generator, defining relator, and
substitution), the reduced relator, Fox derivatives and Alexander polynomial.
The source script recomputes all of these directly from `complexes.json`.
This group certificate is independent of the collapse-to-circle tests used to
prove other spanning edges unknotted.
