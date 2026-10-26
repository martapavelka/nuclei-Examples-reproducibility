# Independent exact orientable dual-graph genus checks (23 October 2026)

This folder verifies the orientable genera of the dual graphs of three nuclei.

N00.txt: N_min, 35 dual vertices, 61 edges, 22 embedding faces, genus 3.
N0.txt: N_CEY, 37 dual vertices, 64 edges, 23 embedding faces, genus 3.
N1.txt: N_BL, 37 dual vertices, 64 edges, 21 embedding faces, genus 4.

The vertices of each dual graph correspond to tetrahedra in input order. Dual edges correspond to shared triangular faces.

## Upper-bound certificates

The *_genus_embedding.json files contain explicit cyclic orders of incident graph edges at each vertex. `verify_embeddings.py` independently reconstructs each dual graph from the facet list, traces the facial cycles of its rotation system, and confirms Euler's formula. No third-party Python packages are required for this check.

    python3 verify_embeddings.py

## Lower-bound SAT tests

The separate script `genus_sat_z3.py` generates a Boolean encoding for whether a connected graph has an orientable rotation system with at least E-V+2-2g facial cycles. It has Boolean variables for local cyclic orders and labels for face orbits of directed edges. A SAT answer represents the existence of such a rotation system. UNSAT rules out genus <=g.

Requires Python 3 and Linux `libz3.so.4` (tested with Z3 4.13.3.0). It does not require the original PySAT script. Commands:

    python3 genus_sat_z3.py N00 2 30
    python3 genus_sat_z3.py N0 2 30
    python3 genus_sat_z3.py N1 3 30

These each returned `UNSAT` in `SAT_run_log.txt`. The adjacent levels (N00 at 3, N0 at 3, N1 at 4) returned SAT in separate test runs and explicit rotation systems were independently verified. The basic sanity tests produce SAT for K4 at genus 0, UNSAT for K5 at genus 0, and SAT for K5 at genus 1. The explicit genus-4 rotation system is independently verifiable with `verify_embeddings.py`.

## Interpretation and limitations

A checked upper-bound rotation system plus SAT-based infeasibility at the next lower genus establishes each reported genus, conditional on the correctness of the SAT encoding and solver. The SAT script is included for inspection and rerunning. No proof-carrying LRAT/DRAT certificate for UNSAT is included, so lower bounds are solver-dependent rather than checked from standalone logical proof objects. The results should be cited as reproducible computer-assisted calculations, not manually proven graph-theoretic lower bounds. To add machine-checkable UNSAT certificates, export the CNF and use a proof-producing SAT solver and checker.

The original `dual_genus.py` in the authors' reproducibility archive is a separate PySAT implementation; this package provides a second implementation using Z3, plus independently checked explicit embeddings. These checks do not resolve separate audit issues regarding nucleus classification or knots.
