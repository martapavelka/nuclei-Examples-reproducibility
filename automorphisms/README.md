# Automorphisms and nine extensions of N00

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The identifiers `N00`, `N0`, `N1` are used in code, data, and certificates.

The automorphism script concerns $N_{\min}$ (`N00`). The extension verifier checks the nine 12-vertex nuclei `M1` through `M9` from `spanning-edges/complexes.json`. All computations use the paper's 1-based vertex labels.

This package independently verifies the claim

    Aut(N00) = {id, sigma} ~= Z/2Z,
    sigma = (1 9)(3 7)(4 11)(5 6)(8 10), with 2 fixed.

## Method

`verify_automorphisms.py` contains the 35 tetrahedral facets of N00 in the
1-based labeling used in the manuscript. It reconstructs edges, triangles,
boundary triangles, and boundary edges directly from those facets.

For each vertex it computes a combinatorial signature consisting of:

1. number of incident tetrahedra;
2. degree in the 1-skeleton;
3. boundary degree;
4. number of incident boundary triangles;
5. the sorted multiset of tetrahedral degrees of incident interior edges.

Every simplicial automorphism must preserve this signature. The signatures
partition the vertices into

    {1,9}, {2}, {3,7}, {4,11}, {5,6}, {8,10}.

Hence only 2^5 = 32 vertex permutations can possibly be automorphisms. The
script tests all 32 exactly by applying each permutation to all 35 facets and
checking equality with the input facet set. Exactly two survive: the
identity and sigma.

The script additionally asserts directly that the displayed sigma preserves
the facet set.

## Run

    python3 verify_automorphisms.py

No third-party Python packages are required.

## Nine extensions and pairwise non-isomorphism

`verify_nine_extensions.py` reconstructs the 18 boundary triangles of `N00`,
checks that the displayed involution partitions them into nine 2-element
orbits, and verifies that the construction faces recorded for `M1`--`M9`
represent these nine orbits exactly once each. For every `Mi`, it rebuilds
the 12-vertex complex from the recorded boundary triangle by replacing
`[a,b,c,x]` with `[a,b,x,12]`, `[a,c,x,12]`, and `[b,c,x,12]`, and checks
its complete facet list against `spanning-edges/complexes.json`.

Pairwise non-isomorphism has a particularly simple certificate. For every
vertex and edge, its **tetrahedral degree** is the number of incident
tetrahedra. Every simplicial isomorphism preserves both the multiset of
vertex tetrahedral degrees and the multiset of edge tetrahedral degrees.
The ordered pairs of these two multisets are different for all nine
complexes. Their degree frequencies are recorded in
`nine_extensions_invariants.json` and recomputed by the verifier.
No graph-isomorphism library or external solver is required.

Run from this directory:

    python3 verify_nine_extensions.py

Together with `verify_automorphisms.py`, these checks certify that there
are precisely nine orbits of boundary attachment triangles, yielding nine
pairwise non-isomorphic nuclei.
