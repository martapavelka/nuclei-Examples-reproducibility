r"""Generate the intrinsic-polyhedron attaching-map illustration (1-skeleton and region attaching maps of
P_{N_min}) as TikZ, directly from the words checked in verify_intrinsic_spines.py.

Output: intrinsic_figure.tex (a tikzpicture, to be \input in the paper; colours
and libraries are set in intrinsic_figure_standalone.tex).
Convention in (b): each boundary arc carries the arrow of its edge e_i;
reading a disk boundary clockwise gives e_i or e_i^{-1} accordingly.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_intrinsic_spines import PAPER_BIG, PAPER_ENDS, letter_ends, is_closed_walk

COL = {1: 'eone', 2: 'etwo', 3: 'ethree', 4: 'efour'}

def disk(cx, word, r, name, idx, start_angle=90):
    """Disk centred at cx with boundary word read clockwise from start_angle."""
    n = len(word)
    out = [f'\\fill[{name}fill] ({cx},0) circle ({r});', f'\\node at ({cx},0) {{$R_{idx}$}};']
    for k, x in enumerate(word):
        a0 = start_angle - 360 * k / n
        a1 = a0 - 360 / n
        mid = (a0 + a1) / 2
        arrow = '>' if x > 0 else '<'     # '>' points clockwise along the arc
        out.append(f'\\draw[{COL[abs(x)]},very thick,decoration={{markings,mark=at position 0.55 with {{\\arrow{{{arrow}}}}}}},'
                   f'postaction={{decorate}}] ({cx},0) ++({a0}:{r}) arc[start angle={a0},end angle={a1},radius={r}];')
        lx, ly = cx + (r + 0.38) * math.cos(math.radians(mid)), (r + 0.38) * math.sin(math.radians(mid))
        out.append(f'\\node[font=\\small] at ({lx:.3f},{ly:.3f}) {{$e_{abs(x)}$}};')
        v = letter_ends(x, PAPER_ENDS)[0]
        vx, vy = cx + r * math.cos(math.radians(a0)), r * math.sin(math.radians(a0))
        out.append(f'\\fill[vert] ({vx:.3f},{vy:.3f}) circle (1.6pt);')
        if True:
            px, py = cx + (r - 0.32) * math.cos(math.radians(a0)), (r - 0.32) * math.sin(math.radians(a0))
            out.append(f'\\node[font=\\scriptsize] at ({px:.3f},{py:.3f}) {{${v[0]}_{v[1]}$}};')
    return out

def skeleton():
    return [
        r'\draw[eone,very thick,mid] (0,0) .. controls (-2.2,1.9) and (-2.2,-1.9) .. (0,0) node[pos=0.5,left,black] {$e_1$};',
        r'\draw[etwo,very thick,mid] (3,0) .. controls (5.2,-1.9) and (5.2,1.9) .. (3,0) node[pos=0.5,right,black] {$e_2$};',
        r'\draw[ethree,very thick,mid] (0,0) to[bend left=35] node[above,black] {$e_3$} (3,0);',
        r'\draw[efour,very thick,mid] (3,0) to[bend left=35] node[below,black] {$e_4$} (0,0);',
        r'\fill[vert] (0,0) circle (1.8pt) node[right=3pt] {$v_1$};',
        r'\fill[vert] (3,0) circle (1.8pt) node[left=3pt] {$v_2$};',
    ]

def main():
    assert is_closed_walk(PAPER_BIG, PAPER_ENDS)
    L = [r'\begin{tikzpicture}[',
         r'  mid/.style={decoration={markings,mark=at position 0.55 with {\arrow{>}}},postaction={decorate}},',
         r'  vert/.style={fill=black!70}]',
         r'\begin{scope}[shift={(0,0)}]']
    L += skeleton()
    L += [r'\node at (1.5,-2.0) {(a)};', r'\end{scope}', r'\begin{scope}[shift={(6.9,0)}]']
    L += disk(0, [1], 0.8, 'Rone', 1, start_angle=-90)
    L += disk(2.4, [2], 0.8, 'Rtwo', 2, start_angle=-90)
    L += disk(5.4, list(PAPER_BIG), 1.45, 'Rthree', 3, start_angle=90)
    L += [r'\node at (2.9,-2.0) {(b)};', r'\end{scope}', r'\end{tikzpicture}']
    (Path(__file__).resolve().parent / 'intrinsic_figure.tex').write_text('\n'.join(L) + '\n')

if __name__ == '__main__':
    main()
