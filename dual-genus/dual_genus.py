#!/usr/bin/env python3
"""
dual_genus.py - orientable genus of the dual graph of a pure simplicial complex.

Dual graph: one node per facet, one edge per ridge shared by exactly two facets
(for a triangulated 3-ball: tetrahedra, joined across interior triangles).

Method (exact):
  * genus is additive over blocks -> split into biconnected components
  * planar blocks: genus 0 (networkx planarity test)
  * other blocks: upper bound U from simulated annealing, then a SAT solver is
    asked whether some rotation system has >= E - V + 2 - 2g faces for
    g = U-1, U-2, ...; the first UNSAT proves the genus (feasibility is
    monotone in g). An Euler/girth lower bound can end the search early.
  * every embedding is re-checked by independent face tracing

Requirements:  pip install networkx python-sat
Inside Sage:   sage -pip install python-sat

Usage:
  python3 dual_genus.py ball.txt [more files ...]
  python3 dual_genus.py ball.txt --cert ball_cert.txt --json ball_cert.json
  python3 dual_genus.py big_ball.txt --timeout 600   # bounds if a level times out
  python3 dual_genus.py ball.txt --anneal 30         # more heuristic time per block
  python3 dual_genus.py --selftest

  From Python/Sage:
    from dual_genus import dual_graph_genus
    res = dual_graph_genus(K.facets())      # K a Sage SimplicialComplex, or
    res = dual_graph_genus([[1,3,4,10], [1,3,5,10], ...])
    res["genus"]

Input format: facets as whitespace-separated vertex lists, one per line,
and/or bracketed lists such as [[1,3,4,10],[1,3,5,10],...] (Lutz-library
style "name=[[...]]" works too). Duplicate facets are ignored, so a file
holding both formats of the same list is fine.
"""
import argparse
import itertools
import json
import math
import random
import re
import sys
import time
from collections import defaultdict

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


# ----------------------------------------------------------------- input ----

def parse_facets(text):
    """Return a list of facets (tuples of vertex labels, as ints when possible)."""
    def conv(tok):
        try:
            return int(tok)
        except ValueError:
            return tok
    facets, seen = [], set()

    def add(tokens):
        if not tokens:
            return
        fac = tuple(conv(t) for t in tokens)
        key = frozenset(fac)
        if key not in seen:
            seen.add(key)
            facets.append(fac)

    for line in text.splitlines():
        line = line.split('#')[0].strip() if '[' not in line else line.strip()
        if not line:
            continue
        if '[' in line:
            for grp in re.findall(r'\[([^\[\]]*)\]', line):
                add([t for t in re.split(r'[,\s]+', grp.strip()) if t])
        elif re.fullmatch(r'-?\d+([\s,]+-?\d+)*', line):
            add([t for t in re.split(r'[,\s]+', line) if t])
    return facets


def dual_graph(facets):
    """Dual graph of a pure complex. Nodes 0..n-1 (index into facets)."""
    facets = [tuple(f) for f in facets]
    sizes = {len(set(f)) for f in facets}
    if len(sizes) != 1:
        raise ValueError(f"complex is not pure: facet sizes {sorted(sizes)}")
    k = sizes.pop()
    if k < 2:
        raise ValueError("facets must have at least 2 vertices")
    ridges = defaultdict(list)
    for i, f in enumerate(facets):
        for r in itertools.combinations(sorted(set(f), key=str), k - 1):
            ridges[r].append(i)
    bad = [r for r, v in ridges.items() if len(v) > 2]
    if bad:
        raise ValueError(f"not a pseudomanifold: {len(bad)} ridge(s) lie in >2 facets, "
                         f"e.g. {bad[0]} in facets {[facets[i] for i in ridges[bad[0]]]}")
    G = nx.Graph()
    G.add_nodes_from(range(len(facets)))
    for r, v in ridges.items():
        if len(v) == 2:
            G.add_edge(*v, ridge=r)
    boundary = sum(1 for v in ridges.values() if len(v) == 1)
    return G, boundary


# ------------------------------------------------------------ embeddings ----

def trace_faces(G, rot):
    """Faces of rotation system rot (rot[v] = cyclic list of neighbours).
    Face tracing rule: dart (a,b) is followed by (b, successor of a around b)."""
    pos = {v: {u: i for i, u in enumerate(r)} for v, r in rot.items()}
    seen, faces = set(), []
    for v in G:
        for u in rot[v]:
            if (v, u) in seen:
                continue
            face, a, b = [], v, u
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                r = rot[b]
                a, b = b, r[(pos[b][a] + 1) % len(r)]
            faces.append(face)
    return faces


def check_rotation(G, rot):
    for v in G:
        if sorted(rot[v], key=str) != sorted(G[v], key=str):
            raise AssertionError(f"rotation at {v} is not a cyclic order of its neighbours")


def genus_of_rotation(G, rot):
    """Genus of the surface of a rotation system on a connected graph."""
    check_rotation(G, rot)
    if G.number_of_edges() == 0:
        return 0
    F = len(trace_faces(G, rot))
    chi = G.number_of_nodes() - G.number_of_edges() + F
    assert chi % 2 == 0
    return (2 - chi) // 2


# ------------------------------------------------------------------ SAT -----

def _exactly_one(lits, pool):
    enc = EncType.pairwise if len(lits) <= 6 else EncType.seqcounter
    return CardEnc.equals(lits, 1, vpool=pool, encoding=enc).clauses


def rotation_with_faces(G, f, solver='cadical153', fix_orientation=True):
    """Rotation system of G with at least f faces, or None if none exists.
    G: connected simple graph, any degrees."""
    nodes = sorted(G, key=str)
    nb = {v: sorted(G[v], key=str) for v in nodes}
    darts = [(v, u) for v in nodes for u in nb[v]]
    nA = len(darts)
    if f < 1 or f > nA:
        return None
    did = {a: i for i, a in enumerate(darts)}
    pool, cl = IDPool(), []

    def q(v, u, k):                  # neighbour u sits at position k around v
        return pool.id(('q', v, u, k))

    def p(v, u, w):                  # w follows u around v
        return pool.id(('p', v, u, w))

    oriented = not fix_orientation
    for v in nodes:
        d = len(nb[v])
        if d <= 2:
            continue
        n0 = nb[v][0]
        cl.append([q(v, n0, 0)])
        cl += [[-q(v, n0, k)] for k in range(1, d)]
        for u in nb[v][1:]:
            cl.append([-q(v, u, 0)])
            cl += _exactly_one([q(v, u, k) for k in range(1, d)], pool)
        for k in range(1, d):
            cl += _exactly_one([q(v, u, k) for u in nb[v][1:]], pool)
        for u in nb[v]:
            for w in nb[v]:
                if u == w:
                    continue
                for k in range(d):
                    k2 = (k + 1) % d
                    cl.append([-q(v, u, k), -q(v, w, k2), p(v, u, w)])
                    cl.append([-p(v, u, w), -q(v, u, k), q(v, w, k2)])
        if not oriented:
            # mirror symmetry: reversing every rotation keeps the face count,
            # and maps positions k -> d-k, so WLOG pos(n1) < pos(n2)
            n1, n2 = nb[v][1], nb[v][2]
            cl += [[-q(v, n1, a), -q(v, n2, b)] for a in range(1, d) for b in range(1, a)]
            oriented = True

    def succ(u, v, w):
        """Literals whose conjunction means 'w follows v around u';
        [] = always, None = never."""
        d = len(nb[u])
        if d == 1:
            return [] if w == v else None
        if d == 2:
            return [] if w != v else None
        return [p(u, v, w)] if w != v else None

    # dart k gets face label x(k,i), i < f; labels are numbered in order of
    # first appearance (i <= k, and label i>0 needs label i-1 on an earlier dart)
    def x(k, i):
        return pool.id(('x', k, i))

    def m(k, i):                     # some dart <= k has label i
        return pool.id(('m', k, i))

    for k in range(nA):
        L = min(f, k + 1)
        cl += CardEnc.equals([x(k, i) for i in range(L)], 1, vpool=pool,
                             encoding=EncType.seqcounter).clauses
        for i in range(L):
            prev = [m(k - 1, i)] if 0 < k and i <= k - 1 else []
            cl.append([-m(k, i), x(k, i)] + prev)
            cl.append([-x(k, i), m(k, i)])
            cl += [[-pr, m(k, i)] for pr in prev]
            if i > 0:
                cl.append([-x(k, i), m(k - 1, i - 1)])
    cl.append([x(k, f - 1) for k in range(f - 1, nA)])      # all f labels used
    for (v, u) in darts:                                     # labels closed under tracing
        k = did[(v, u)]
        for w in nb[u]:
            s = succ(u, v, w)
            if s is None:
                continue
            k2 = did[(u, w)]
            for i in range(min(f, k + 1)):
                cl.append([-x(k, i)] + [-l for l in s] + ([x(k2, i)] if i <= k2 else []))

    with Solver(name=solver, bootstrap_with=cl) as S:
        if not S.solve():
            return None
        model = set(l for l in S.get_model() if l > 0)
    rot = {}
    for v in nodes:
        d = len(nb[v])
        if d <= 2:
            rot[v] = list(nb[v])
        else:
            rot[v] = sorted(nb[v], key=lambda u: next(k for k in range(d) if q(v, u, k) in model))
    return rot


# ------------------------------------------------------------- heuristic ----

def _anneal_once(G, seconds, rng, target):
    nodes = list(G)
    rot = {v: list(G[v]) for v in nodes}
    for v in nodes:
        rng.shuffle(rot[v])
    pos = {v: {u: i for i, u in enumerate(rot[v])} for v in nodes}

    def nxt(a, b):
        r = rot[b]
        return (b, r[(pos[b][a] + 1) % len(r)])

    def count_through(darts):
        seen, c = set(), 0
        for d in darts:
            if d in seen:
                continue
            c += 1
            x = d
            while x not in seen:
                seen.add(x)
                x = nxt(*x)
        return c

    F = count_through([(v, u) for v in nodes for u in rot[v]])
    best, best_rot = F, {v: list(r) for v, r in rot.items()}
    movable = [v for v in nodes if G.degree(v) >= 3]
    if not movable:
        return best, best_rot
    T0, T, t0, it = 1.5, 1.5, time.time(), 0
    while best < target:
        it += 1
        if it % 256 == 0:
            frac = (time.time() - t0) / seconds
            if frac >= 1:
                break
            T = max(0.05, T0 * (1 - frac))
        v = rng.choice(movable)
        inc = [(a, v) for a in rot[v]]          # darts whose successor depends on rot[v]
        before = count_through(inc)
        i, j = rng.sample(range(len(rot[v])), 2)
        rot[v][i], rot[v][j] = rot[v][j], rot[v][i]
        pos[v][rot[v][i]], pos[v][rot[v][j]] = i, j
        dF = count_through(inc) - before
        if dF >= 0 or rng.random() < math.exp(dF / T):
            F += dF
            if F > best:
                best, best_rot = F, {w: list(r) for w, r in rot.items()}
        else:
            rot[v][i], rot[v][j] = rot[v][j], rot[v][i]
            pos[v][rot[v][i]], pos[v][rot[v][j]] = i, j
    return best, best_rot


def anneal_rotation(G, seconds=5.0, restarts=3, seed=0, target=None):
    """Simulated annealing over rotation systems, maximising the face count
    (incremental face recount per move). Heuristic: returns (faces, rotation),
    i.e. an upper bound on the genus. Stops early once `target` faces is reached."""
    target = float('inf') if target is None else target
    best_F, best_rot = -1, None
    for r in range(restarts):
        F, rot = _anneal_once(G, seconds / restarts, random.Random(seed + r), target)
        if F > best_F:
            best_F, best_rot = F, rot
        if best_F >= target:
            break
    return best_F, best_rot


# ---------------------------------------------------------------- genus -----

def _worker(conn, G, f, solver):
    conn.send(rotation_with_faces(G, f, solver=solver))
    conn.close()


def rotation_with_faces_timed(G, f, solver='cadical153', timeout=None):
    """Like rotation_with_faces, but returns 'timeout' if not decided within
    `timeout` seconds (runs in a child process, since CaDiCaL cannot be interrupted)."""
    if not timeout:
        return rotation_with_faces(G, f, solver=solver)
    import multiprocessing as mp
    parent, child = mp.Pipe(duplex=False)
    proc = mp.Process(target=_worker, args=(child, G, f, solver), daemon=True)
    proc.start()
    child.close()
    if parent.poll(timeout):
        res = parent.recv()
        proc.join()
        return res
    proc.terminate()
    proc.join()
    return 'timeout'


def _block_genus(B, solver, log, timeout=None, anneal_seconds=5.0, seed=0):
    """Returns (lower, upper, rotation realising upper); lower == upper unless
    a SAT call timed out.
    1. lower bound L from Euler's formula with the girth
    2. upper bound U from simulated annealing (or a trivial rotation)
    3. descend: ask SAT for genus U-1, U-2, ...; UNSAT at U-1 proves genus = U
       (feasibility is monotone, so a single UNSAT settles it)
    4. if a descent call times out, climb from L to raise the lower bound"""
    V, E = B.number_of_nodes(), B.number_of_edges()
    planar, emb = nx.check_planarity(B)
    if planar:
        return 0, 0, {v: list(emb.neighbors_cw_order(v)) for v in B}
    girth = nx.girth(B)
    fmax = (2 * E) // girth                     # every face walk has length >= girth
    L = max(1, math.ceil((E - V + 2 - fmax) / 2))
    log(f"    Euler/girth lower bound: {L}  (girth {girth})")
    t = time.time()
    if anneal_seconds and anneal_seconds > 0:
        _, rot = anneal_rotation(B, anneal_seconds, seed=seed, target=E - V + 2 - 2 * L)
    else:
        rot = {v: list(B[v]) for v in B}
    U = genus_of_rotation(B, rot)
    log(f"    heuristic upper bound: {U}  [{time.time() - t:.1f}s]")

    def ask(g):
        f = E - V + 2 - 2 * g
        t = time.time()
        r = rotation_with_faces_timed(B, f, solver=solver, timeout=timeout)
        ans = 'timeout' if r == 'timeout' else ('yes' if r else 'no')
        log(f"    genus <= {g}? (>= {f} faces): {ans}  [{time.time() - t:.1f}s]")
        return r

    # descend from the upper bound
    stuck = False
    while U > L:
        r = ask(U - 1)
        if r == 'timeout':
            stuck = True
            break
        if r is None:
            return U, U, rot                    # UNSAT at U-1: genus = U
        rot, U = r, genus_of_rotation(B, r)
    if not stuck:
        return U, U, rot                        # reached the lower bound
    # climb from the lower bound to tighten it
    while L < U - 1:
        r = ask(L)
        if r == 'timeout':
            break
        if r is None:
            L += 1
        else:                                   # all levels below L were UNSAT
            return L, L, r
    return L, U, rot


def graph_genus(G, solver='cadical153', log=print, timeout=None, return_bounds=False,
                anneal_seconds=5.0, seed=0):
    """Orientable genus of G (sum over connected components) plus a rotation
    system realising it. Genus is additive over blocks (Battle-Harary-Kodama-Youngs);
    block rotations are glued at cut vertices by concatenation."""
    total, low, rot = 0, 0, {v: [] for v in G}
    blocks = [B for B in nx.biconnected_components(G)]
    log(f"  {len(blocks)} block(s); sizes (V,E): "
        + ", ".join(f"({len(B)},{G.subgraph(B).number_of_edges()})"
                    for B in sorted(blocks, key=len, reverse=True)[:8])
        + (" ..." if len(blocks) > 8 else ""))
    for B in blocks:
        H = G.subgraph(B).copy()
        if H.number_of_edges() == 0:
            continue
        if H.number_of_edges() <= 2:            # bridge
            lB, gB, rB = 0, 0, {v: list(H[v]) for v in H}
        else:
            if H.number_of_edges() > 3 and not nx.check_planarity(H)[0]:
                log(f"  non-planar block with {H.number_of_nodes()} nodes, {H.number_of_edges()} edges:")
            lB, gB, rB = _block_genus(H, solver, log, timeout, anneal_seconds, seed)
        total += gB
        low += lB
        for v, r in rB.items():
            rot[v] += r
    # independent check: face tracing on every component
    g_check = sum(genus_of_rotation(G.subgraph(c), {v: rot[v] for v in c})
                  for c in nx.connected_components(G))
    assert g_check == total, f"embedding check failed: {g_check} != {total}"
    if return_bounds:
        return low, total, rot
    if low != total:
        raise RuntimeError(f"only bounds {low} <= genus <= {total} (timeout)")
    return total, rot


def dual_graph_genus(facets, solver='cadical153', log=print, timeout=None,
                     anneal_seconds=5.0, seed=0):
    """Main entry point. Returns a dict with genus (None if only bounds were
    obtained), genus_lower, genus_upper, graph data and the embedding.
    timeout: seconds per SAT call (None = no limit, result is exact).
    anneal_seconds: time for the heuristic upper bound per block (0 = off)."""
    facets = [tuple(f) for f in facets]
    G, boundary = dual_graph(facets)
    degs = sorted(d for _, d in G.degree())
    log(f"  facets {len(facets)}, dim {len(facets[0]) - 1}, dual graph V={G.number_of_nodes()} "
        f"E={G.number_of_edges()}, boundary ridges {boundary}, connected {nx.is_connected(G)}")
    log(f"  degree counts: " + ", ".join(f"{d}:{degs.count(d)}" for d in sorted(set(degs))))
    lo, up, rot = graph_genus(G, solver=solver, log=log, timeout=timeout, return_bounds=True,
                              anneal_seconds=anneal_seconds, seed=seed)
    faces = trace_faces(G, rot) if G.number_of_edges() else []
    return dict(genus=up if lo == up else None, genus_lower=lo, genus_upper=up,
                facets=facets, graph=G, boundary_ridges=boundary, rotation=rot, faces=faces)


# ---------------------------------------------------------------- output ----

def write_cert_txt(res, path, source=""):
    G, rot, facets = res['graph'], res['rotation'], res['facets']
    lab = lambda i: f"t{i + 1}"
    V, E, F = G.number_of_nodes(), G.number_of_edges(), len(res['faces'])
    c = nx.number_connected_components(G)
    L = [f"Dual graph genus certificate {source}".rstrip(),
         "Nodes: facets t1..tn in input order. Edges: ridges shared by two facets.",
         f"V = {V}, E = {E}, faces = {F}, components = {c}, boundary ridges = {res['boundary_ridges']}",
         (f"Genus = {res['genus']}   (V - E + F = {V - E + F} = 2*{c} - 2*{res['genus']})"
          if res['genus'] is not None else
          f"Bounds: {res['genus_lower']} <= genus <= {res['genus_upper']}  (SAT timeout; embedding below realises the upper bound)"),
         "Lower bound: SAT solver proved no rotation system has more faces (see log).",
         "", "Facets:"]
    L += [f"{lab(i)}: {' '.join(map(str, f))}" for i, f in enumerate(facets)]
    L += ["", "Rotation system (cyclic neighbour order; faces traced by (a,b) -> (b, next of a at b)):"]
    L += [f"{lab(v)}: " + " ".join(lab(u) for u in rot[v]) for v in sorted(G)]
    L += ["", f"Faces ({F}):"]
    L += [f"[{len(fc)}] " + " ".join(lab(x) for x in fc) for fc in res['faces']]
    with open(path, 'w') as fh:
        fh.write("\n".join(L) + "\n")


def write_cert_json(res, path):
    G = res['graph']
    out = dict(genus=res['genus'], genus_lower=res['genus_lower'], genus_upper=res['genus_upper'], facets=[list(f) for f in res['facets']],
               edges=[[a + 1, b + 1] for a, b in G.edges()],
               rotation={str(v + 1): [u + 1 for u in res['rotation'][v]] for v in sorted(G)},
               faces=[[x + 1 for x in fc] for fc in res['faces']],
               note="node i = i-th facet (1-based)")
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1)


# -------------------------------------------------------------- selftest ----

def _brute_genus(G):
    """Exhaustive over all rotation systems (small connected graphs only)."""
    vs = list(G)
    opts = [[[list(G[v])[0]] + list(pm) for pm in itertools.permutations(list(G[v])[1:])]
            if G.degree(v) > 1 else [list(G[v])] for v in vs]
    best = 0
    for choice in itertools.product(*opts):
        best = max(best, len(trace_faces(G, dict(zip(vs, choice)))))
    return (2 - (G.number_of_nodes() - G.number_of_edges() + best)) // 2


def selftest(seconds=120):
    quiet = lambda *a, **k: None
    ok = True
    known = [('octahedron', nx.octahedral_graph(), 0), ('K5', nx.complete_graph(5), 1),
             ('K3,3', nx.complete_bipartite_graph(3, 3), 1), ('K4,4', nx.complete_bipartite_graph(4, 4), 1),
             ('K6', nx.complete_graph(6), 1), ('K7', nx.complete_graph(7), 1), ('K8', nx.complete_graph(8), 2),
             ('Petersen', nx.petersen_graph(), 1), ('Heawood', nx.heawood_graph(), 1),
             ('Pappus', nx.pappus_graph(), 1), ('Q4', nx.hypercube_graph(4), 1),
             ('Desargues', nx.desargues_graph(), 2),
             ('Tutte 8-cage', nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5), 4),
             ('2 x K5 at a vertex', nx.compose(nx.complete_graph(5),
                                              nx.relabel_nodes(nx.complete_graph(5), {i: i + 4 for i in range(5)})), 2)]
    print("known genera:")
    for name, G, exp in known:
        G = nx.convert_node_labels_to_integers(G)
        t = time.time()
        g, _ = graph_genus(G, log=quiet, anneal_seconds=0.5)
        g0, _ = graph_genus(G, log=quiet, anneal_seconds=0)
        g = g if g == g0 else f"{g}/{g0}"
        ok &= (g == exp)
        print(f"  {name:20s} {g}  expected {exp}  {'ok' if g == exp else 'FAIL'}  [{time.time() - t:.1f}s]")
    print(f"random graphs vs brute force ({seconds}s):")
    rng = random.Random(1)
    n, bad, hist, t0 = 0, 0, {}, time.time()
    while time.time() - t0 < seconds:
        if rng.random() < 0.5:                  # sparse, mixed degrees
            nv = rng.randint(5, 10)
            G = nx.gnm_random_graph(nv, rng.randint(nv, 2 * nv + 2), seed=rng.randint(0, 10**9))
        else:                                   # denser, aims at genus >= 2
            d, nv = rng.choice([(3, 14), (3, 16), (4, 7)])
            G = nx.random_regular_graph(d, nv, seed=rng.randint(0, 10**9))
        if not nx.is_connected(G) or max(d for _, d in G.degree()) > 5:
            continue
        size = math.prod(math.factorial(max(d - 1, 0)) for _, d in G.degree())
        if size > 300_000:
            continue
        gb, (gs, _) = _brute_genus(G), graph_genus(G, log=quiet, anneal_seconds=rng.choice([0, 0.1]))
        n += 1
        hist[gb] = hist.get(gb, 0) + 1
        if gb != gs:
            bad += 1
            ok = False
            print("  MISMATCH", gb, gs, list(G.edges()))
    print(f"  {n} graphs, {bad} mismatches, genus histogram {dict(sorted(hist.items()))}")
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return ok


# ------------------------------------------------------------------ main ----

def main():
    ap = argparse.ArgumentParser(description="Orientable genus of the dual graph of a pure simplicial complex.")
    ap.add_argument('files', nargs='*', help="facet list files")
    ap.add_argument('--cert', help="write text certificate (single input file)")
    ap.add_argument('--json', help="write JSON certificate (single input file)")
    ap.add_argument('--solver', default='cadical153', help="PySAT solver name (default cadical153)")
    ap.add_argument('--timeout', type=float, default=None,
                    help="seconds per SAT call; on timeout, report lower/upper bounds instead")
    ap.add_argument('--anneal', type=float, default=5.0,
                    help="seconds of simulated annealing per block for the upper bound (0 = off)")
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--selftest', action='store_true', help="validate against known genera and brute force")
    ap.add_argument('--selftest-seconds', type=int, default=120)
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest(a.selftest_seconds) else 1)
    if not a.files:
        ap.error("give at least one file, or --selftest")
    if (a.cert or a.json) and len(a.files) > 1:
        ap.error("--cert/--json need a single input file")
    for path in a.files:
        print(f"{path}:")
        t = time.time()
        facets = parse_facets(open(path).read())
        res = dual_graph_genus(facets, solver=a.solver, timeout=a.timeout,
                               anneal_seconds=a.anneal, seed=a.seed)
        if res['genus'] is not None:
            print(f"  GENUS = {res['genus']}   ({len(res['faces'])} faces, {time.time() - t:.1f}s)")
        else:
            print(f"  BOUNDS: {res['genus_lower']} <= genus <= {res['genus_upper']}   ({time.time() - t:.1f}s)")
        if a.cert:
            write_cert_txt(res, a.cert, source=f"for {path}")
            print(f"  certificate -> {a.cert}")
        if a.json:
            write_cert_json(res, a.json)
            print(f"  json -> {a.json}")


if __name__ == '__main__':
    main()
