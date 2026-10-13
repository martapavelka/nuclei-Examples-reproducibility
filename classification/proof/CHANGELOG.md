# Changes in the current classification note

1. Identified `N00` with the paper's `N_min`, explaining the label shift 0,...,10 to 1,...,11.
2. Separated the independent all-interior-edge-tetrahedron theorem from the computational argument.
3. Clarified that every MILP condition is necessary, not sufficient.
4. Explained why excluding tetrahedron vectors alone gives exhaustive enumeration: all auxiliary variables are determined by the tetrahedron vector.
5. Preserved and checked the original v=11 count table (1,829 fillings; one 35-tetrahedron nucleus), and added its explicit provenance.
6. Independently reran the v<=10 enumeration (306 infeasible models) and provided the boundary files and run log.
7. Strengthened the collapse checker to check all higher-dimensional cofaces, not only codimension-one cofaces; all 89 collapse pairs still verify.
8. Added a standalone positive topology checker for the N00 facet list, links, boundary, homology, and f-vector.
9. Clearly distinguished the rerun results from the recorded v=11 classification counts and the lack of independently checkable solver UNSAT certificates.
