# src/parser.py

from src.oracle_static import oracle
from src.transitions_arc_eager import transition
from src.debug_utils import print_state
from src.projectivize import projectivize


def attach_orphans(arcs, n):
    attached = [d for _, d, _ in arcs]
    for i in range(1, n):
        if i not in attached:
            arcs.append((0, i, "root"))


def parse(words, heads, labels, debug=False):
    """
    Arc-eager parser with:
    - static oracle
    - optional debug
    - optional projectivization
    """

    # ---------- PROJECTIVIZATION ----------
    gold_arcs = [(heads[i], i, labels[i]) for i in range(1, len(words))]
    gold_arcs = projectivize(gold_arcs)

    for h, d, l in gold_arcs:
        heads[d] = h
        labels[d] = l
    # --------------------------------------

    stack = [0]
    buffer = [i for i in range(1, len(words))]
    arcs = []

    step = 0

    while buffer:
        trans = oracle(stack, buffer, heads, labels, arcs)

        if debug:
            print_state(step, stack.copy(), buffer.copy(), trans, arcs.copy())

        stack, buffer, arcs = transition(trans, stack, buffer, arcs)
        step += 1

    attach_orphans(arcs, len(words))
    return arcs
