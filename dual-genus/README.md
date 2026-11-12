# Exact orientable genera of the dual graphs

The complexes `N00`, `N0`, `N1` correspond to the manuscript's
$N_{\min}$, $N_{\mathrm{CEY}}$, and $N_{\mathrm{BL}}$, respectively.
The input files `N00.txt`, `N0.txt`, and `N1.txt` list the tetrahedra using
1-based vertex labels. The dual graph has one vertex per tetrahedron and
one edge per interior triangle.

## Results

| Complex | Dual vertices | Dual edges | Orientable genus | Embedding faces | Excluded genus |
| --- | ---: | ---: | ---: | ---: | --- |
| `N00` | 35 | 61 | 3 | 22 | at most 2 |
| `N0` | 37 | 64 | 3 | 23 | at most 2 |
| `N1` | 37 | 64 | 4 | 21 | at most 3 |

The `independent-z3/` directory provides explicit orientable rotation
systems and a standard-library verifier, together with a separate Z3
Boolean encoding for lower-genus feasibility and its execution results.
The `dual_genus.py` program provides another implementation using
NetworkX and PySAT. The rotation systems certify the upper bounds; the
lower bounds rely on the correctness of the supplied SAT programs and
solvers. No independently checkable UNSAT proof objects are included.

## Verification

```bash
python3 independent-z3/verify_embeddings.py
python3 independent-z3/genus_sat_z3.py K4 0 30
python3 independent-z3/genus_sat_z3.py K5 0 30
python3 independent-z3/genus_sat_z3.py K5 1 30
python3 independent-z3/genus_sat_z3.py N00 2 120
python3 independent-z3/genus_sat_z3.py N0 2 120
python3 independent-z3/genus_sat_z3.py N1 3 120
```

The control tests return `SAT`, `UNSAT`, and `SAT`, respectively;
the three nucleus tests return `UNSAT`. A solver timeout or `UNKNOWN`
does not establish the lower bound. The Z3 script locates a system
installation of the Z3 shared library or the `z3-solver` Python package.
See `independent-z3/README.md` for additional instructions.

To rerun the independent PySAT implementation from this directory:

```bash
pip install -r requirements.txt
./run_all.sh
```

`dual_graph_summaries.json` records the combinatorial graph sizes;
`RESULT_STATUS.json` points to the checkable embeddings and solver results.
`N00_exact_run.log` records an additional PySAT result for `N00`.
