# Nuclei: reproducibility of Section 3

Repository: https://github.com/martapavelka/nuclei-Examples-reproducibility

Computational data, verification programs, certificates, and recorded results for the examples and classification in Section 3 of the paper on **nuclei of triangulated 3-balls**.

**What is in this repository:** the six original reproducibility packages as browsable directories, without nested ZIPs or compiled Python caches. Their source files, data, results, documentation, and per-package SHA256 manifests are preserved. Each directory has a more detailed README with the exact proof and verification scope.

## Names and vertex labels

| Identifier in programs/data | Name in the paper | Meaning |
| --- | --- | --- |
| `N00` | $N_{\min}$ | Unique nontrivial nucleus with 11 vertices, 35 tetrahedra |
| `N0` | $N_{\mathrm{CEY}}$ | 12-vertex example of Collet–Eckmann–Younan |
| `N1` | $N_{\mathrm{BL}}$ | 12-vertex example of Benedetti–Lutz |
| `M1`, ..., `M9` | $N_{\min}^{(1)},\ldots,N_{\min}^{(9)}$ | Nine 12-vertex extensions of $N_{\min}$ |

**Vertex-label convention:** `classification/results/n00_facets.json` uses 0-based labels; add 1 to compare with the paper. The other packaged facet lists generally use 1-based labels. See each README. The old identifiers are retained inside code and data to preserve the original checks and recorded outputs.

## Contents

| Directory | Scope | Key entry point |
| --- | --- | --- |
| [`classification/`](classification/) | Lower bound of 11 vertices, 11-vertex classification, MILP enumeration, 89-step collapse certificate | `src/verify_n00_collapse_strict.py`, `src/verify_n00_positive.py`, `src/nucleus_lower_bound.py`, `src/classify_v11.py` |
| [`unique-boundary-filling/`](unique-boundary-filling/) | Only nucleus filling of the boundary of $N_{\min}$ | `search_fixed_boundary.py` |
| [`automorphisms/`](automorphisms/) | $\mathrm{Aut}(N_{\min})\cong C_2$ | `verify_automorphisms.py` |
| [`spanning-edges/`](spanning-edges/) | Unknotted spanning-edge checks for $N_{\min}$ and its nine extensions | `verify_spanning_edges.py` |
| [`trefoil-edges/`](trefoil-edges/) | Trefoil certificates for edges $\{9,11\}$ of $N_{\mathrm{CEY}}$ and $\{2,3\}$ of $N_{\mathrm{BL}}$ | `verify_inputs.py`, `certify_trefoil_edges.py` |
| [`dual-genus/`](dual-genus/) | Dual-graph genus computations for the three named examples | `dual_genus.py`, `run_all.sh` |

The trefoil package repeats some of the spanning-edge package's original data and source so that **each package remains independently usable**.

## Start here: inexpensive checks

Python 3 is required. The basic classification and automorphism verifiers use the standard library; the positive verification uses the bundled classification program and may require NumPy and SciPy. Trefoil reconstruction requires SymPy.

From the repository root:

```bash
python3 automorphisms/verify_automorphisms.py
python3 classification/src/verify_n00_collapse_strict.py classification/results/n00_collapse_certificate.json
python3 classification/src/verify_n00_positive.py
python3 trefoil-edges/verify_inputs.py
python3 scripts/verify_checksums.py
```

For a single command running these checks, use `python3 scripts/quick_check.py` (see its output for skipped/missing dependencies).

## Recomputing the longer results

Install the Python dependencies you need (a fresh virtual environment is recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-recommended.txt
```

To recompute trefoil certificates:

```bash
cd trefoil-edges
python3 certify_trefoil_edges.py
```

The command above **regenerates and overwrites** `trefoil_certificates.json`. Run it in a clean working tree or a copy if you want to compare recorded output.

To rerun the lower-bound search, from `classification/` build the bundled `plantri` source and run:

```bash
mkdir -p build
unzip src/plantri-master.zip -d build
make -C build/plantri-master plantri
python3 src/nucleus_lower_bound.py --plantri build/plantri-master/plantri --min-v 4 --max-v 10 --out reproduced_lower_bound
```

For the exhaustive **11-vertex classification** run, use `classification/src/classify_v11.py` with the same `plantri` executable and consult [`classification/README.md`](classification/README.md). That search can take substantial time. Similarly, the fixed-boundary search, all-edge collapses, and exact dual-genus SAT search can take a long time. Their README files give their precise commands and limitations.

For exact orientable genus, `dual-genus/dual_genus.py` uses NetworkX and PySAT, including an available SAT backend (default `cadical153`). **The preserved `dual-genus/requirements.txt` from the research archive is empty**; use the new root `requirements-recommended.txt` to install the required packages. Simply finding a rotation system establishes an upper bound; an exact genus claim additionally depends on the lower-bound SAT result.

## Computational verification status

The packaged **v=4,...,10** enumeration was rerun (306 boundary types and no feasible instances). The stored **v=11** enumeration totals 1,829 candidate fillings, one surviving nucleus, and an 89-step positive collapse certificate. The complete expensive v=11 enumeration **was not independently rerun for the October 2026 revision**; see [`classification/README.md`](classification/README.md) for that distinction.

For the dual-graph genera, recorded claims are 3 for $N_{\min}$, 3 for $N_{\mathrm{CEY}}$, and 4 for $N_{\mathrm{BL}}$. The precise provenance and which SAT runs were replayed are documented in [`dual-genus/README.md`](dual-genus/README.md) and [`dual-genus/RESULT_STATUS.json`](dual-genus/RESULT_STATUS.json). In particular, the historical genus-3 result for $N_{\min}$ is recorded as a user-supplied SAT run transcript; no independent UNSAT certificate is bundled.

The combinatorial and algebraic verifiers reproduce **computational witnesses**; their mathematical implications additionally use the topological lemmas discussed in the individual package READMEs. No solver-independent proof objects are claimed for MILP infeasibility or SAT UNSAT conclusions.

## Integrity and provenance

Every package contains its own `SHA256SUMS` (or `SHA256SUMS.txt`) for its research files. `python3 scripts/verify_checksums.py` checks all six. The per-package files are not renamed or rewritten to preserve these checksums; the top-level documentation and checking scripts are new. Build products (`__pycache__`, `.pyc`), generated outputs, and local virtual environments are not part of the versioned release.

## Citation and reuse

When using these computations, please cite **the associated nuclei paper** as well as any underlying works named in its bibliography. Add the final paper title, authors, DOI/arXiv URL, and version here when public.

**Licensing has not yet been specified by the authors.** The bundled `plantri` source is a third-party component and may have its own licensing and attribution requirements. Please do not assume that a license applied to original scripts would also apply to `plantri`; refer to its bundled upstream files.
