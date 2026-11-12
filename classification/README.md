# Smallest nontrivial nucleus: classification and reproducibility

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The identifiers `N00`, `N0`, and `N1` appear in filenames, data, and scripts.

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

* [plantri](https://users.cecs.anu.edu.au/~bdm/plantri/): third-party planar triangulation generator,
  obtained separately from its official distribution (not bundled).
* `src/nucleus_lower_bound.py`: common sphere parser, MILP formulation,
  exact combinatorial checker, and v=4,...,10 driver.
* `src/classify_v11.py`: full v=11 exhaustion driver, 14<=t<=36,
  with no-good cuts over the tetrahedron indicator vectors.
* `src/verify_n00_collapse.py`: collapse certificate checker.
* `src/verify_n00_collapse_strict.py`: standalone checker that
  tests **all cofaces** and checks facets
  against the canonical N00 file.
* `src/verify_n00_positive.py`: check the canonical 35 tetrahedra, stored
  boundary representative, incidence conditions, links, homology, and f-vector.
* `data/boundaries_v4.asc`, ..., `data/boundaries_v10.asc`:
  lower-bound boundary lists, included with checksums.
* `data/boundaries_v11.asc`: 1,249 boundary representatives.
* `results/lower_bound_v4_v10_run.json`: v<=10 run results,
  including all 306 infeasible cases and program/input hashes.
* `results/expected_counts.json`: v=11 enumeration counts.
* `results/n00_facets.json`: N00 facets, with vertices 0,...,10.
* `results/n00_collapse_certificate.json`: 89 collapse pairs.
* `results/search_summary.md`: v=11 outcome summary.
* `proof/nucleus_vertex_classification.tex` and `.pdf`: proof note.
* `SHA256SUMS.txt`: SHA256 hashes for distributed source/data/proof files.

In the main paper N00 is called `N_min` and the vertex labels are 1,...,11.
Add 1 to each label in the stored facets to obtain the main paper's facet list.
The v=11 survivor occurs at boundary representative index 689 (zero-based).

## Repeat the computations

Requires Python 3, NumPy and SciPy (HiGHS), and a separately downloaded
and compiled `plantri` executable. Get `plantri` from the
[official distribution](https://users.cecs.anu.edu.au/~bdm/plantri/) and follow its build instructions.
The stored `data/boundaries_v*.asc` files remain included, so the
recorded boundary lists can be checked without installing `plantri`.

```bash
# Set this to the path of the separately installed plantri executable.
PLANTRI=/absolute/path/to/plantri

python src/nucleus_lower_bound.py \
  --plantri "$PLANTRI" \
  --min-v 4 --max-v 10 --out reproduced_lower_bound

python src/classify_v11.py \
  --plantri "$PLANTRI" \
  --out reproduced_v11.json

python src/verify_n00_collapse_strict.py \
  results/n00_collapse_certificate.json
python src/verify_n00_positive.py
sha256sum -c SHA256SUMS.txt
```

The stored `results/lower_bound_v4_v10_run.json` records the path and
checksum of the plantri executable used for that run. That recorded path is
not a file distributed with this repository. Any separately installed
plantri executable can be supplied via `--plantri` when rerunning the search.

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

## Computational scope and limitations

For $4\le v\le10$, the search covers all 306 boundary spheres and
finds no feasible filling. The complete 11-vertex enumeration using the supplied
`src/classify_v11.py` driver and an independent CP-SAT/Regina
implementation yields identical counts and the same unique nucleus.
The independent implementation is not distributed in this repository. The stored counts are summaries,
not individually checkable solver proof objects.

The positive nucleus checks and the 89-step elementary-collapse certificate
are directly replayable. Negative results depend on the correctness of
`plantri`, the binary model, and the HiGHS solver; no MILP infeasibility
proof objects are included.
