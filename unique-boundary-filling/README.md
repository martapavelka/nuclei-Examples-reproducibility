# Unique nucleus filling of the boundary of N00

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The original `N00`, `N0`, `N1`
identifiers remain in filenames, JSON keys, scripts, commands, logs, and
certificates so that the computational evidence can be reproduced unchanged.

This archive concerns **only** $N_{\min}$ (`N00`); the facet list uses labels $1,\ldots,11$.

This package reproduces the computer-assisted verification that the 18-triangle boundary sphere of N00 has exactly one filling that is both a nucleus and a triangulated 3-ball: N00 itself.

## Requirements

- Python 3
- NumPy
- SciPy with `scipy.optimize.milp`

## Run

```bash
python search_fixed_boundary.py
```

The script reads only `N00_facets.txt`, reconstructs the boundary as the triangles occurring in exactly one tetrahedron, and then builds the finite 0-1 MILP model.

It checks every tetrahedron count t=14,...,36. The model enforces the prescribed boundary, degree 0/2 for nonboundary triangles, the nucleus reducedness restriction, activation of interior edges, the general tetrahedron upper bound, existence of an all-interior tetrahedron, and Euler characteristic 1 for every vertex link. Every enumerated incidence solution is then independently checked for the exact boundary, triangle incidences, reducedness, dual connectivity, disk vertex links, interval/circle edge links, and mod-2 homology.

Expected manifold-candidate counts:

- t=14,...,32: 0
- t=33: 1, Betti vector (1,1,1,0)
- t=34: 4, all Betti vector (1,1,1,0)
- t=35: 4; three have (1,1,1,0), one has (1,0,0,0)
- t=36: 0

The unique candidate with ball homology is asserted to have exactly the original N00 facet set. Since N00 is independently verified to be a triangulated 3-ball, while every other manifold candidate has nontrivial H_1 and H_2 over F_2, N00 is the unique nucleus/3-ball filling of this boundary.

`run.log` and `results.json` are retained outputs of the included run.
