# Reproducibility package: orientable genus of the dual graphs of N00, N0, N1

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The original `N00`, `N0`, `N1`
identifiers remain in filenames, JSON keys, scripts, commands, logs, and
certificates so that the computational evidence can be reproduced unchanged.

The input files `N00.txt`, `N0.txt`, and `N1.txt` are the facet lists of $N_{\min}$, $N_{\mathrm{CEY}}$, and $N_{\mathrm{BL}}$, respectively. All three use vertex labels starting at 1.

## Purpose
This package reproduces the orientable graph-genus computation for the dual graphs of three nuclei. A dual-graph vertex is a tetrahedron; two dual vertices are adjacent exactly when the tetrahedra share an interior triangle.

## Contents
- `N00.txt`, `N0.txt`, `N1.txt`: complete tetrahedron lists.
- `dual_genus.py`: the supplied exact genus program.
- `N00_exact_run.log`: verbatim user-provided exact rerun output establishing genus 3 for N00.
- `dual_graph_summaries.json`: independently reconstructed basic graph data, requiring no SAT solver.
- `run_all.sh`: one-command reproduction, including the program's self-test.
- `requirements.txt`: Python dependencies.
- `RESULT_STATUS.json`: deliberately separates previously reported results from what is certified in the present runtime.
- `original_N0_Sage_notebook.ipynb`: original exploratory Sage notebook supplied by the authors; it contains N0 and calls `flip_graph().genus()`, but has no saved genus output.
- `SHA256SUMS`: integrity hashes.

## Method
`dual_genus.py` constructs the dual graph, decomposes it into biconnected blocks (orientable genus is additive over blocks), handles planar blocks directly, finds an upper-bound rotation system by simulated annealing, and uses SAT to ask whether a rotation system with sufficiently many faces exists at smaller genus. An UNSAT answer one level below a realized upper bound proves optimality. Every returned embedding is independently rechecked by face tracing and Euler characteristic.

This is stronger than merely finding a drawing/rotation of a certain genus: an embedding certifies an **upper bound**, while exactness requires the lower-bound/SAT part (or another rigorous lower bound).

## Reproduce
Use a normal Python environment with internet/package access:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_all.sh
```

For a long exact run without a SAT timeout, `run_all.sh` deliberately does not pass `--timeout`. The default PySAT backend requested by the program is `cadical153`. You can select another installed PySAT solver with `--solver`.

## Result status at package creation
- **N0:** previously computed in this project as orientable dual-graph genus **3**. The package contains the exact input and solver needed to reproduce/certify this independently.
- **N1:** previously computed in this project as orientable dual-graph genus **4**. The package contains the exact input and solver needed to reproduce/certify this independently.
- **N00:** exact orientable dual-graph genus **3**. A user rerun of `dual_genus.py` found a genus-3 rotation system with 22 faces (`genus <= 3? yes`) and the SAT solver returned UNSAT for genus at most 2 (`genus <= 2? no`, requiring at least 24 faces). Hence `genus(N00)=3`. The verbatim supplied transcript is archived as `N00_exact_run.log`.

## Environment limitation during package creation
The package-creation runtime had NetworkX but neither PySAT nor Sage, and outbound package installation was unavailable. The exact N00 SAT result was therefore produced by the user on a separate environment and its verbatim console transcript is archived here. The package-creation runtime did not independently rerun that SAT computation.

## Independent sanity data
`dual_graph_summaries.json` was generated independently of `dual_genus.py` directly from the facet lists. It checks the number of dual vertices/edges, boundary triangles, connectivity, and degree distribution.

## Publication recommendation
For a paper, retain the generated `*_run.log`, `*_certificate.txt`, and `*_certificate.json` from the exact rerun. The text/JSON rotation system is independently checkable as an upper-bound embedding. For the lower bound, archive the solver version and complete run log. Note that `dual_genus.py` currently relies on the SAT solver's UNSAT answer; it does not emit a DRAT/LRAT proof object. If proof-carrying SAT is desired, the next upgrade should export CNF and a machine-checkable UNSAT certificate.
