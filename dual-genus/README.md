# Reproducibility package: orientable genus of the dual graphs of N00, N0, N1

Updated 24 October 2026 to incorporate the independent verification of 23 October 2026. This README replaces the original `dual-genus/README.md`. The original source files and provenance are retained.

## Notation and input

The names used in the paper and in the computations correspond as follows:

`N00` denotes $N_{\min}$, `N0` denotes $N_{\mathrm{CEY}}$ (Collet, Eckmann, and Younan), and `N1` denotes $N_{\mathrm{BL}}$ (Benedetti and Lutz). These are the same three nuclei, not additional examples. The computational identifiers are preserved in all filenames and logs.

The files `N00.txt`, `N0.txt`, and `N1.txt` contain the complete tetrahedron lists, with vertices numbered from 1. The dual graph has one vertex for each tetrahedron and one edge for each shared interior triangle. Its genus is the **orientable graph genus**.

## Verified results and their scope

**N00 ($N_{\min}$):** 35 dual vertices, 61 dual edges, and an explicitly verified rotation system with 22 facial cycles, giving genus 3. The independent Z3 test returned UNSAT for genus at most 2. The original PySAT run also reports genus 3 in `N00_exact_run.log`.

**N0 ($N_{\mathrm{CEY}}$):** 37 dual vertices, 64 dual edges, and an explicitly verified rotation system with 23 facial cycles, giving genus 3. The independent Z3 test returned UNSAT for genus at most 2.

**N1 ($N_{\mathrm{BL}}$):** 37 dual vertices, 64 dual edges, and an explicitly verified rotation system with 21 facial cycles, giving genus 4. The independent Z3 test returned UNSAT for genus at most 3.

The explicit rotation systems independently certify the upper bounds by face tracing and Euler's formula. The lower bounds rely on the correctness of the included SAT encoding and solver. No independently checkable DRAT/LRAT proof objects of UNSAT are provided; these are reproducible **computer-assisted** exact-genus results, not solver-independent lower-bound certificates. See `RESULT_STATUS.json` for per-example provenance and status.

## Contents of the original package

`N00.txt`, `N0.txt`, `N1.txt` contain the facet lists. `dual_genus.py` is the original PySAT-based genus program. `run_all.sh` runs its self-test and exact computations. `requirements.txt` lists the original Python dependencies. `dual_graph_summaries.json` contains independently reconstructed graph data. `N00_exact_run.log` records the earlier author-supplied exact PySAT output. `original_N0_Sage_notebook.ipynb` is exploratory provenance, without stored genus output. `PROVENANCE.txt` records the origin and limitations of the original files. `SHA256SUMS` is the original integrity manifest.

The original `dual_genus.py` constructs the dual graph, decomposes it into biconnected blocks, searches for upper-bound rotation systems, and tests lower genus through SAT. As in the original package, its output depends on the PySAT backend. A timed-out SAT test yields bounds rather than a proof of exact genus.

## Additional folder: independent-verification/

Copy the **contents** of `Nuclei_Dual_Genus_Independent_Verification_2026-10-23/` from the independent verification archive into a new `dual-genus/independent-verification/` directory. Do not replace or delete the original files.

This folder contains `N00_genus_embedding.json`, `N0_genus_embedding.json`, and `N1_genus_embedding.json`, with explicit cyclic orders of dual edges; `verify_embeddings.py`, which reconstructs the graphs and checks each rotation system without third-party dependencies; `genus_sat_z3.py`, a separate Boolean encoding tested using system Z3; `SAT_run_log.txt` and `embedding_checks_log.txt`, which record the 23 October results; and separate input lists, checksums, and its own detailed `README.md`.

The original and independent programs use the same facet lists. The independent SAT program is **not** a replacement for the original PySAT implementation.

## Reproduce the original PySAT calculations

From `dual-genus/`, in a Python environment with package installation available:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_all.sh
```

`run_all.sh` executes the program's self-test and then processes N00, N0, and N1 without imposing a SAT timeout. The default requested PySAT backend is `cadical153`. Generated files include `N00_run.log`, `N0_run.log`, `N1_run.log`, plus `*_certificate.txt` and `*_certificate.json`. The original package did not include complete PySAT execution logs for N0 or N1, and the separate original N00 transcript is retained as historical provenance.

## Reproduce the independent checks

From `dual-genus/independent-verification/`:

```bash
python3 verify_embeddings.py
python3 genus_sat_z3.py K4 0 30
python3 genus_sat_z3.py K5 0 30
python3 genus_sat_z3.py K5 1 30
python3 genus_sat_z3.py N00 2 30
python3 genus_sat_z3.py N0 2 30
python3 genus_sat_z3.py N1 3 30
```

The embedding checker requires only Python 3. The SAT script requires the Linux shared library `libz3.so.4`; the archived tests used Z3 4.13.3.0. `30` is the per-test timeout in seconds, not a guarantee that the tests will finish in that time in every environment. The three nucleus tests should return `UNSAT`; the control checks should return `SAT` for K4 genus 0, `UNSAT` for K5 genus 0, and `SAT` for K5 genus 1. Treat `UNKNOWN` or a timeout as inconclusive.

The Z3 checks and rotation-system verification were rerun successfully on 24 October 2026. The execution transcript from 23 October remains in `independent-verification/SAT_run_log.txt`.

## Integrity and release preparation

The original `SHA256SUMS` contains hashes of the **old** `README.md` and `RESULT_STATUS.json`; replacing those files makes the original checksum entries stale. After adding `independent-verification/` and replacing these two files, regenerate the parent manifest. Run from `dual-genus/`:

```bash
find . -type f ! -name SHA256SUMS ! -path './.venv/*' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
sha256sum -c SHA256SUMS
```

This hashes the current package, including any logs and certificates already in the directory; run it after finalizing the released contents. Preserve the historical transcripts, provenance, solver versions, and exact released commit or archive checksum. The independent solver does not generate proof-carrying UNSAT certificates; producing and checking such certificates would strengthen the lower-bound evidence further.
