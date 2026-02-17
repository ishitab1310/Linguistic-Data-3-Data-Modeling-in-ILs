from src.constants import SH, RE, RA, LA
from src.transitions_arc_eager import has_head


def dependents_in_buffer(token, buffer, heads):
    return any(heads[b] == token for b in buffer)


def oracle(stack, buffer, heads, labels, arcs):
    if stack and buffer:
        s = stack[0]
        b = buffer[0]

        # LEFT ARC
        if heads[s] == b and not has_head(s, arcs):
            return (LA, labels[s])

        # RIGHT ARC
        if heads[b] == s:
            return (RA, labels[b])

    # REDUCE
    if stack:
        s = stack[0]
        if has_head(s, arcs) and not dependents_in_buffer(s, buffer, heads):
            return (RE, "_")

    return (SH, "_")
