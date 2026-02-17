def crossing(a, b):
    h1, d1, _ = a
    h2, d2, _ = b

    a1, a2 = sorted([h1, d1])
    b1, b2 = sorted([h2, d2])

    return a1 < b1 < a2 < b2


def is_projective(arcs):
    for i in range(len(arcs)):
        for j in range(i + 1, len(arcs)):
            if crossing(arcs[i], arcs[j]):
                return False
    return True


def projectivize(arcs):
    arcs = arcs.copy()

    while not is_projective(arcs):
        for i, (h, d, l) in enumerate(arcs):
            if h != 0:
                arcs[i] = (0, d, l)  
                break

    return arcs
