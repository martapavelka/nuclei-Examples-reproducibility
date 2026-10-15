# Intrinsic spines and evasiveness of three nuclei

This supplement uses the facet lists in `complexes.json`, copied unchanged from
`Nmin_NCEY_NBL_trefoil_reproducibility.zip`. The original working names are
`N00 = N_min`, `N0 = N_CEY`, and `N1 = N_BL`.

## Intrinsic polyhedra

Run `python3 verify_intrinsic_spines.py`.

The program finds all interior edges and triangles, reconstructs the singular
locus from interior triangles with all three edges interior, joins the dual
polygons across regular dual edges, and traces the attaching word of each
region. It checks the resulting words, up to cyclic rotation, orientations,
and admissible edge relabeling, against the presentation of Bing's house in
Fagan, Qiu and Wang (2026, Section 3.3.2).

For N_min it obtains the four-edge graph with adjacency matrix
`[[2,2],[2,2]]`, with one loop at each of two vertices and two connecting
edges. The three region attaching words have lengths `1, 1, 10`. After an
orientation-preserving relabeling of paths, the length-ten word is

    3 -1 -3 2 -1 -2 -4 2 -3 -4

and the remaining disk boundary words are `4` and `-1`, up to independent
orientation reversal of disks. This is precisely the Bing's-house presentation
in Fagan--Qiu--Wang, not its mutant.

For N_CEY and N_BL the singular locus has one vertex and two loops, and their
intrinsic polyhedra each have two disk regions. Since both are spines of the
3-ball, these agree with the unique complexity-one 3-ball spine, the abalone.

Reference: Lucas Fagan, Yang Qiu, Zhenghan Wang, *Classification of Cellular
Fake Surfaces*, Journal of Experimental Mathematics 2(1):155-171, 2026.
https://doi.org/10.56994/JXM.002.001.006

## Evasiveness

Run `python3 verify_evasiveness.py`.

The program uses the standard recursive definition: a simplex is non-evasive;
a nonsimplex is non-evasive only if some vertex has both a non-evasive deletion
and a non-evasive link. It explores every possible choice with memoization. It
uses no homological pruning or non-collapsibility assumption.

All three nuclei are evasive. The computation visits 3,403 recursive states
for N_min, 3,633 for N_CEY and 3,903 for N_BL (state counts under this exact
implementation).

## Important figure correction

The previously generated schematic `DnPn.png` incorrectly draws four parallel
singular edges between two vertices. The actual singular graph of P_Nmin has
one loop at each vertex and two connecting edges. It should not be used as a
literal picture of P_Nmin until corrected.
