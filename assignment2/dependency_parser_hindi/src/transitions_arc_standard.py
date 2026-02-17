from src.constants import SH, RA, LA


def transition(trans, stack, buffer, arcs):
    action, label = trans

    if action == SH:
        stack.insert(0, buffer.pop(0))

    elif action == LA:
        h = stack[0]
        d = stack[1]
        arcs.append((h, d, label))
        stack.pop(1)

    elif action == RA:
        h = stack[1]
        d = stack[0]
        arcs.append((h, d, label))
        stack.pop(0)

    return stack, buffer, arcs
