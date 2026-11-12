# Intrinsic spines and evasiveness of three nuclei

This supplement includes the facet lists of the three nuclei in `complexes.json`.
The computational identifiers are `N00 = N_min`, `N0 = N_CEY`, and `N1 = N_BL`.

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
edges. The three region attaching words have lengths `1, 1, 10`. After a
relabeling of the paths (reversing orientations where needed), the
length-ten word is

    3 -1 -3 2 -1 -2 -4 2 -3 -4

and the remaining disk boundary words are `4` and `-1`, up to independent
orientation reversal of disks. This is precisely the Bing's-house presentation
in Fagan--Qiu--Wang, not its mutant. In this presentation the loops are `1`
and `4` and the connecting edges are `2` and `3`.

### Attaching-map labelling (Figure 12 in the paper)

The script also prints the words in the labelling of the manuscript figure:
`e1` is the loop at `v1`, `e2` the loop at `v2`, `e3: v1 -> v2` and
`e4: v2 -> v1`, with `v1 = [4,6,8,10]` and `v2 = [5,8,10,11]`.
The Fagan--Qiu--Wang names translate as

    1 -> e1,   2 -> e3^-1,   3 -> e4,   4 -> e2

and the attaching maps are

    dR1 = e1
    dR2 = e2
    dR3 = e4 e1^-1 e4^-1 e3^-1 e1^-1 e3 e2^-1 e3^-1 e4^-1 e2^-1

The script checks that each word is a closed walk in the graph and that
every edge lies on exactly three region sides. It also checks that the
computed words are these words for some choice of names.

Run `python3 make_intrinsic_figure.py` to produce `intrinsic_figure.tex`,
a TikZ construction directly from the verified attaching words.
`intrinsic_figure_standalone.tex` compiles the source independently.
`PNminMaps.png` is the illustration included in the current manuscript
(Figure 12); the TikZ construction encodes the same attaching maps.
In (b), each arc carries the orientation of its edge, so the boundary
word can be read from the labelled arcs.

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
