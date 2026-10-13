# Automorphism group of N00

## Notation in the paper

The manuscript denotes the complexes as follows: `N00` = $N_{\min}$,
`N0` = $N_{\mathrm{CEY}}$ (Collet--Eckmann--Younan), and `N1` =
$N_{\mathrm{BL}}$ (Benedetti--Lutz). These are alternate names for the
same complexes, not additional examples. The original `N00`, `N0`, `N1`
identifiers remain in filenames, JSON keys, scripts, commands, logs, and
certificates so that the computational evidence can be reproduced unchanged.

This archive concerns **only** $N_{\min}$ (`N00`); its automorphism script uses the paper's vertex labels $1,\ldots,11$.

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
checking equality with the original facet set. Exactly two survive: the
identity and sigma.

The script additionally asserts directly that the displayed sigma preserves
the facet set.

## Run

    python3 verify_automorphisms.py

No third-party Python packages are required.
