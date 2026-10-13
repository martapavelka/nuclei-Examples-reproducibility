# Smallest nontrivial nucleus: classification and reproducibility

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The original `N00`, `N0`, `N1`
identifiers remain in filenames, JSON keys, scripts, commands, logs, and
certificates so that the computational evidence can be reproduced unchanged.

The unique 11-vertex nucleus is stored as `N00` ($N_{\min}$). Its canonical `results/n00_facets.json` uses labels $0,\ldots,10$, so add 1 to obtain the paper's labels $1,\ldots,11$. The package also includes the exhaustive boundary searches, but not the `N0` or `N1` facet lists.

The document `proof/nucleus_vertex_classification.tex` gives the computer-assisted
classification of nontrivial nuclei by vertex number. It uses an independently
proved structural theorem: every nontrivial nucleus contains a tetrahedron
with six interior edges.

**Main result:** No nontrivial nucleus has fewer than 11 vertices. At 11
vertices there is, up to simplicial isomorphism, exactly one, denoted
`N_min` in the manuscript and `N00` in the data. It has 35 tetrahedra and
f-vector `(11, 54, 79, 35)`.

## Package contents

* `src/plantri-master.zip`: source of the planar triangulation generator.
* `src/nucleus_lower_bound.py`: common sphere parser, MILP formulation,
  exact combinatorial checker, and v=4,...,10 driver.
* `src/classify_v11.py`: full v=11 exhaustion driver, 14<=t<=36,
  with no-good cuts over the tetrahedron indicator vectors.
* `src/verify_n00_collapse.py`: original collapse certificate checker.
* `src/verify_n00_collapse_strict.py`: strengthened standalone checker that
  tests **all cofaces**, not only codimension-one cofaces, and checks facets
  against the canonical N00 file.
* `src/verify_n00_positive.py`: check the canonical 35 tetrahedra, stored
  boundary representative, incidence conditions, links, homology, and f-vector.
* `data/boundaries_v4.asc`, ..., `data/boundaries_v10.asc`: regenerated
  lower-bound boundary lists, included with checksums.
* `data/boundaries_v11.asc`: original 1,249 boundary representatives.
* `results/lower_bound_v4_v10_run.json`: new complete v<=10 run record,
  including all 306 infeasible cases and program/input hashes.
* `results/expected_counts.json`: original **reported** v=11 counts.
* `results/n00_facets.json`: N00 facets, with vertices 0,...,10.
* `results/n00_collapse_certificate.json`: 89 collapse pairs.
* `results/search_summary.md`: original v=11 outcome summary.
* `proof/nucleus_vertex_classification.tex` and `.pdf`: updated proof.
* `SHA256SUMS.txt`: SHA256 hashes for distributed source/data/proof files.

In the main paper N00 is called `N_min` and the vertex labels are 1,...,11.
Add 1 to each label in the stored facets to obtain the main paper's facet list.
The v=11 survivor occurs at boundary representative index 689 (zero-based).

## Repeat the computations

Requires a C compiler, `make`, Python 3, NumPy and SciPy (HiGHS).

```bash
unzip src/plantri-master.zip -d build
make -C build/plantri-master plantri

python src/nucleus_lower_bound.py \
  --plantri build/plantri-master/plantri \
  --min-v 4 --max-v 10 --out reproduced_lower_bound

python src/classify_v11.py \
  --plantri build/plantri-master/plantri \
  --out reproduced_v11.json

python src/verify_n00_collapse_strict.py \
  results/n00_collapse_certificate.json
python src/verify_n00_positive.py
sha256sum -c SHA256SUMS.txt
```

The `classify_v11.py` command is an exhaustive run and can be expensive.  Do
not set debug search limits when reproducing the theorem.

## Reported v=11 classification counts

| t | feasible fillings | nuclei |
|:--|--:|--:|
| 14--29 | 0 | 0 |
| 30 | 8 | 0 |
| 31 | 54 | 0 |
| 32 | 213 | 0 |
| 33 | 504 | 0 |
| 34 | 623 | 0 |
| 35 | 360 | 1 |
| 36 | 67 | 0 |
| Total | 1,829 | 1 |

All 1,828 rejected fillings were reported to have mod-2 Betti vector
`(1,1,1,0)`; the unique survivor has `(1,0,0,0)`.

## Verification status and limitations

For the current revision (October 2026), the **entire v=4,...,10 run** was
independently rerun from the packaged `plantri` source and Python driver:
306 boundary types, zero feasible fillings, no truncated searches.
Regenerating `plantri -a11` also exactly reproduced the stored v=11
boundary file. The **positive N00 checks** and 89 collapse steps were
replayed, including tests for all cofaces in each elementary collapse.

The **complete v=11 solver enumeration was not rerun** for this revision:
its table is from the earlier recorded computation and is reproducible
using `src/classify_v11.py`. The supplied `expected_counts.json` is a
summary, not a record of the individual solver decisions.

All negative computational results depend on correctness of `plantri`,
the model implementation, and HiGHS. No independently checkable UNSAT/MILP
infeasibility certificates are provided. The positive collapse sequence
is independently checkable without HiGHS.
