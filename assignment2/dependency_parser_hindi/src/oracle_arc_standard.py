from src.constants import SH, LA, RA


def oracle(stack, buffer, heads, labels):
    if len(stack) >= 2:
        s0 = stack[0]
        s1 = stack[1]

        # LEFT ARC
        if heads[s1] == s0:
            return (LA, labels[s1])

        # RIGHT ARC
        if heads[s0] == s1:
            return (RA, labels[s0])

    if buffer:
        return (SH, "_")

    return None
