# Reproducibility materials: Counting Triangulated 3-Spheres, Nuclei, and Polyhedra

This repository contains executable checks, data, and certificates for
*Counting Triangulated 3-Spheres, Nuclei, and Polyhedra* by Bergfinnur
Durhuus and Marta Pavelka. It includes the computer-assisted classification,
explicit examples, knot certificates, intrinsic-polyhedron reconstruction,
evasiveness checks, orientable dual-graph genus calculations, and a
nonuniqueness example for boundary-edge reduction to atoms.

## Identifiers and vertex labels

| Dataset identifier | Paper identifier | Meaning |
| --- | --- | --- |
| `N00` | $N_{\min}$ | Unique 11-vertex nontrivial nucleus (35 tetrahedra) |
| `N0` | $N_{\mathrm{CEY}}$ | 12-vertex nucleus of Collet, Eckmann, and Younan |
| `N1` | $N_{\mathrm{BL}}$ | 12-vertex nucleus obtained from the Benedetti–Lutz ball |
| `M1` ... `M9` | $N_{\min}^{(1)}$ ... $N_{\min}^{(9)}$ | Nine 12-vertex extensions |

**Vertex labels:** `classification/results/n00_facets.json` uses labels
0 through 10. Add 1 to compare with the paper's tables. Other facet files
use 1-based labels as documented in their directories. These identifiers
are fixed by the included source and data.

## Directory contents

| Directory | Main checks |
| --- | --- |
| `classification/` | Vertex lower bound, exhaustive 11-vertex enumeration, collapse certificate |
| `unique-boundary-filling/` | Unique 3-ball nucleus filling of the boundary of $N_{\min}$ |
| `automorphisms/` | $\mathrm{Aut}(N_{\min})\cong C_2$; nine boundary-triangle orbits and pairwise non-isomorphic 12-vertex extensions |
| `spanning-edges/` | Unknotted spanning-edge certificates and nine extensions |
| `trefoil-edges/` | Trefoil certificates for $N_{\mathrm{CEY}}$ and $N_{\mathrm{BL}}$ |
| `dual-genus/` | Dual graph orientable genera 3, 3, and 4 (PySAT and Z3) |
| `nuclei_intrinsic_spines_and_evasiveness/` | Intrinsic polyhedra, region attaching words, Figure 12 (intrinsic-polyhedron attaching maps), evasiveness |
| `atom-reduction-nonuniqueness/` | Explicit counterexample to uniqueness of atom reduction, with facet lists and contraction certificates |
| `scripts/` | Repository-wide quick checks and SHA256 manifest verification |

## Quick verification

Run the following from the repository root:

```bash
python3 scripts/quick_check.py
```

For the optional computations, install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-recommended.txt
```

Detailed instructions, stored results, computational assumptions, and
limitations are provided in each directory's `README.md`. The expensive
exhaustive searches and SAT infeasibility checks are not part of the quick
verification command.

## Mathematical scope

The verification scripts establish finite combinatorial claims and supply
explicit certificates. Their topological interpretations require standard
PL topology, as described in the paper and the package READMEs. The
classification and SAT-based genus lower bounds depend on the correctness
of the encodings and solvers; independently checkable UNSAT/MILP proof
objects are not included. Rotation systems, collapse certificates, and the boundary-edge
contraction/non-contraction certificates are independently checkable positive witnesses.

## Integrity and citation

`python3 scripts/verify_checksums.py` checks the SHA256 manifests for all
research directories. Cite the paper and an immutable release or commit of
this repository when reusing these results.

`plantri` is a third-party program by Gunnar Brinkmann and Brendan McKay,
with contributions from Heidi Van den Camp. Its source code is **not bundled**.
Download it separately from the [official plantri website](https://users.cecs.anu.edu.au/~bdm/plantri/)
if reproducing the classification; see `classification/README.md`.
A licence for the authors' original code and materials should be specified
by the authors before a licensing claim is made.
