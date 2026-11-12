# N00 and M1--M9 spanning-edge reproducibility package

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The identifiers `N00`, `N0`, `N1` are used in code, data, and certificates.

This directory contains `N00` and `M1`--`M9`, but not `N0` or `N1`. The working identifiers `M1`--`M9` denote the nine nuclei $N_{\min}^{(1)},\ldots,N_{\min}^{(9)}$ in the paper. All stored facets use labels starting at 1.

This package records and reproduces the spanning-edge calculations for the 11-vertex nucleus `N00` and the nine 12-vertex nuclei `M1,...,M9` obtained from it by the boundary attachment + 2-to-3 construction. Their pairwise non-isomorphism and the nine distinct boundary-triangle orbits are certified in `../automorphisms/verify_nine_extensions.py`.

## Contents

- `complexes.json` — complete 1-based facet lists for `N00,M1,...,M9`, construction faces, removed tetrahedra, opposite vertices, and new spanning edges.
- `verify_spanning_edges.py` — pure-Python (standard library only) independent verifier. By default it checks the single new edge of `M1,...,M9`; with `--all-edges` it checks every spanning edge of selected complexes.
- `REDUCTION_LEMMA.md` — PL reduction explaining why old spanning edges retain their knot type and why only `[x,12]` is new.
- `results_M4_all_edges.json`, `results_M5_all_edges.json`, `results_M6_all_edges.json` — recorded complete 28-edge interactive runs.
- `results_M7_M9_new_edges.json` — recorded interactive certificates for the three final new edges.
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

Together with the old-edge reduction, it is enough to check the one new edge in each `Mi`. The PL reduction is logically separate from the computational certificate.

## Scope of included results

The included JSON files give full 28-edge checks for `M4`, `M5` and `M6` and checks of the new edges of `M7` through `M9`. Checks of the new edges of `M1` through `M3` and all spanning edges of `N00` are reproducible using the provided verifier, but their result JSONs are not included. The acceptance condition is an explicit collapse to a connected rank-one graph; collapse counts can depend on deterministic tie-breaking.
