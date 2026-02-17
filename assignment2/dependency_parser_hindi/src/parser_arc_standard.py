from src.oracle_arc_standard import oracle
from src.transitions_arc_standard import transition


def parse(words, heads, labels):
    stack = []
    buffer = [i for i in range(len(words))]
    arcs = []

    while buffer or len(stack) > 1:
        trans = oracle(stack, buffer, heads, labels)

        if trans is None:
            break

        stack, buffer, arcs = transition(trans, stack, buffer, arcs)

    return arcs
