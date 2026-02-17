def print_state(step, stack, buffer, action, arcs):
    act = action[0]
    label = action[1]

    if label != "_":
        act_str = f"{act}({label})"
    else:
        act_str = str(act)

    print(
        f"STEP {step:02d} | "
        f"STACK={stack} | "
        f"BUFFER={buffer} | "
        f"ACTION={act_str} | "
        f"ARCS={arcs}"
    )
