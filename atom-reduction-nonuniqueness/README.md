# Nonuniqueness of atom reduction under boundary-edge contractions

This directory provides an explicit counterexample to the order-independence statement in M. Younan, *Dynamics and Combinatorics of 2 and 3 Dimensional Triangulations* (2014), Lemma 4.1.4, under the admissibility criterion of Lemma 3.5.14. This does not by itself refute the counting theorem for atoms.

## Exact construction

`Nmin_facets.txt` gives the 35 tetrahedra of the vertex-minimal nucleus $N_{\min}$, with labels 1,...,11, exactly as in Table 1 of Durhuus and Pavelka, *Counting Triangulated 3-Spheres, Nuclei, and Polyhedra*. All facet lists in this directory are complete; each line specifies the four vertex labels of one tetrahedron. Labels are 1-based throughout.

Construct $G=N_{\min}\sharp N_{\min}$ by taking two copies, identifying their boundary triangle `[1,2,3]`, relabelling the second copy's remaining vertices `i -> i + 8` for `4 <= i <= 11`, and performing the 2-to-3 move across the common triangle. The two removed tetrahedra are `[1,2,3,11]` and `[1,2,3,19]`; insert `[1,2,11,19]`, `[1,3,11,19]`, `[2,3,11,19]`. This yields `G_facets.txt` (19 vertices, 71 tetrahedra).

Perform the stellar subdivision of the **boundary edge** `[1,2]` of $G$ by inserting vertex 20. Replace each tetrahedron `[1,2,a,b]` by `[1,20,a,b]` and `[2,20,a,b]`. Specifically, the three subdivided tetrahedra are `[1,2,8,11]`, `[1,2,11,19]`, and `[1,2,16,19]`. The result is `H_facets.txt` (20 vertices, 74 tetrahedra).

Both `[1,20]` and `[8,20]` are admissible boundary-edge contractions in $H$ under Younan's three stated conditions:

* Contracting `[1,20]` (sending 20 to 1) returns $G$ exactly (19 vertices, 71 tetrahedra).
* Contracting `[8,20]` (sending 20 to 8) gives `K_facets.txt` (19 vertices, 72 tetrahedra).

Both $G$ and $K$ satisfy the nucleus condition, are triangulated PL 3-balls, and have **no further admissible boundary-edge contractions**. As their tetrahedron counts differ, they are nonisomorphic atoms. Therefore the two maximal contraction sequences terminate at different atoms.

## Verification

```sh
python3 -m pip install -r requirements.txt
python3 verify.py
python3 verify_artifacts.py
```

`verify.py` reconstructs the complexes from the 35 source tetrahedra, checks the three vertex links of every boundary edge contraction (in particular the full link intersection criterion), checks that every vertex link is a connected triangulated disk and the boundary is a connected triangulated sphere, checks connectivity of the tetrahedron dual graph and the nucleus condition, and exhaustively checks all boundary edges for further contractions. The contraction criterion includes vertex, edge, and face intersections; the script also verifies that identifying the endpoints produces a genuine simplicial quotient without leftover lower-dimensional faces or repeated tetrahedra.

`verify_artifacts.py` cross-checks **all five exact tetrahedron lists** against the generated complexes and independently validates `atom_witnesses.txt`: for each of the 51 boundary edges of $G$ and of $K$, the certificate names a common neighbour $c$ for which `[a,c]` and `[b,c]` are edges but `[a,b,c]` is not a triangle. This proves that the relevant edge fails Younan's first contraction condition. In particular, there is no need to assume that checking one specific contraction order is exhaustive.

The topological 3-ball assertion also follows without computer-assisted 3-manifold recognition: $G$ is obtained by gluing two PL 3-balls along a triangle and applying a 2-to-3 bistellar move; $H$ is a stellar subdivision of $G$; and the two admissible link-condition contractions preserve the PL homeomorphism type. The script independently checks the required local manifold and boundary conditions.

`SHA256SUMS` records the checksums for the input files and verification code. Recompute using `sha256sum -c SHA256SUMS` from this directory.
