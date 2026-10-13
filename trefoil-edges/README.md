# N00 and M1--M9 spanning-edge reproducibility package

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The original `N00`, `N0`, `N1`
identifiers remain in filenames, JSON keys, scripts, commands, logs, and
certificates so that the computational evidence can be reproduced unchanged.

This archive contains all three named nuclei, plus `M1`--`M9` (the paper's $N_{\min}^{(1)},\ldots,N_{\min}^{(9)}$). In particular, the trefoil certificates for `N0` and `N1` concern edges $\{9,11\}$ of $N_{\mathrm{CEY}}$ and $\{2,3\}$ of $N_{\mathrm{BL}}$, respectively. Stored facets use the paper's 1-based vertex labels.

This package records and reproduces the spanning-edge calculations for the 11-vertex nucleus `N00` and the nine 12-vertex nuclei `M1,...,M9` obtained from it by the boundary attachment + 2-to-3 construction.

## Contents

- `complexes.json` — complete 1-based facet lists for `N00,M1,...,M9`, construction faces, removed tetrahedra, opposite vertices, and new spanning edges.
- `verify_spanning_edges.py` — pure-Python (standard library only) independent verifier. By default it checks the single new edge of `M1,...,M9`; with `--all-edges` it checks every spanning edge of selected complexes.
- `REDUCTION_LEMMA.md` — PL reduction explaining why old spanning edges retain their knot type and why only `[x,12]` is new.
- `results_M4_all_edges.json`, `results_M5_all_edges.json`, `results_M6_all_edges.json` — recorded complete 28-edge interactive runs.
- `results_M7_M9_new_edges.json` — recorded interactive certificates for the three final new edges.
- `PROVENANCE.txt` — scope and provenance of the recorded outputs.
- `SHA256SUMS` — hashes of package files.

## Reproduce the economical proof

Run the nine new-edge checks:

    python3 verify_spanning_edges.py --output reproduced_new_edges.json

The verifier constructs the barycentric exterior of the selected spanning edge by deleting the barycentric vertices corresponding to the two endpoints and the edge itself. It then performs explicit elementary simplicial collapses.

A computational PASS means the terminal complex is literally 1-dimensional and connected with `beta1=1`. Thus the exterior collapses to a connected rank-one graph.

To rerun all 28 spanning edges of, for example, `M6`:

    python3 verify_spanning_edges.py --complex M6 --all-edges --output reproduced_M6.json

To rerun all spanning edges of `N00`:

    python3 verify_spanning_edges.py --complex N00 --all-edges --output reproduced_N00.json

## Mathematical conclusion and topological input

The computation supplies explicit collapse certificates. The manuscript should state/cite separately the standard PL-topological implication used after the computation: the relevant exterior is a compact PL 3-manifold; collapsing to a connected rank-one graph makes it a genus-one handlebody (solid torus), and a properly embedded spanning arc in `B^3` with solid-torus exterior is unknotted.

Together with the old-edge reduction, it is enough to check the one new edge in each `Mi`. The package intentionally keeps this PL reduction logically separate from the computational certificate.

## Recorded-results caveat

The files for `M4`, `M5`, and `M6` record complete interactive 28-edge runs. `M7`--`M9` record the final new-edge runs. Earlier interactive checks of `M1`--`M3` are not copied into a precomputed JSON here because their full improved-routine logs were not retained in the current runtime; they are reproducible directly from `complexes.json` with the included verifier. No missing log is presented as a certificate.

Collapse counts and final graph sizes depend on the deterministic collapse choices in the implementation. The invariant acceptance condition is the explicit collapse to a connected rank-one graph.

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
