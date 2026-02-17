from src.constants import SH, RE, RA, LA


def has_head(token, arcs):
    return any(d == token for _, d, _ in arcs)


def transition(trans, stack, buffer, arcs):
    action, label = trans

    # SHIFT
    if action == SH:
        stack.insert(0, buffer.pop(0))

    # REDUCE
    elif action == RE:
        if stack:
            stack.pop(0)

    # RIGHT ARC
    elif action == RA:
        head = stack[0]
        dep = buffer[0]
        arcs.append((head, dep, label))
        stack.insert(0, buffer.pop(0))

    # LEFT ARC
    elif action == LA:
        head = buffer[0]
        dep = stack.pop(0)
        arcs.append((head, dep, label))

    return stack, buffer, arcs
