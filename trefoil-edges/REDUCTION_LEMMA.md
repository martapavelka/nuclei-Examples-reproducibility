# Reduction for old spanning edges

Let `N` be a triangulated 3-ball, let `F=[a,b,c]` be a boundary triangle, and let `[a,b,c,x]` be its unique incident tetrahedron. Introduce a new boundary vertex `y` and replace

    [a,b,c,x]

by

    [a,b,x,y], [a,c,x,y], [b,c,x,y].

Geometrically this is the same PL 3-ball with the boundary triangle `F` stellarly subdivided by `y`. The local replacement admits a PL homeomorphism to the original tetrahedron that is the identity on the common part of the boundary and carries every old edge to the corresponding old arc. Hence the knot type of every old spanning edge is unchanged. The only spanning edge not inherited from `N` is `[x,y]`.

Accordingly, once all spanning edges of `N00` are known to be unknotted, proving the same statement for each `Mi` reduces to checking its single new edge `[x,12]`.

This lemma does **not** assert that `[x,12]` is locally boundary-parallel. That tempting stronger claim is false as an immediate local argument here: for the nine representatives the edges from `x` to the vertices of `F` are interior edges. The new edge is therefore checked separately by the exterior-collapse computation.
