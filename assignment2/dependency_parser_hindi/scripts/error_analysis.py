"""
Automatic parser error analysis.
Compares gold vs predicted trees.
"""

def read_file(path):
    sentences = []
    sent = []

    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()

            if not line:
                if sent:
                    sentences.append(sent)
                sent = []
                continue

            cols = line.split("\t")
            if len(cols) >= 4:
                sent.append(cols)

    return sentences


def analyze(gold_path, pred_path):
    gold = read_file(gold_path)
    pred = read_file(pred_path)

    total = 0
    head_errors = 0
    label_errors = 0
    root_errors = 0

    for gs, ps in zip(gold, pred):
        for g, p in zip(gs, ps):

            total += 1

            g_head = g[2]
            p_head = p[2]

            g_label = g[3]
            p_label = p[3]

            if g_head != p_head:
                head_errors += 1

            if g_label != p_label:
                label_errors += 1

            if g_head == "0" and p_head != "0":
                root_errors += 1

    print("\n===== ERROR ANALYSIS =====")
    print(f"Total tokens: {total}")
    print(f"Head errors: {head_errors}")
    print(f"Label errors: {label_errors}")
    print(f"Root attachment errors: {root_errors}")
    print(f"UAS: {(total-head_errors)/total:.4f}")
    print(f"LAS: {(total-max(head_errors,label_errors))/total:.4f}")


if __name__ == "__main__":
    analyze("data/en-ud-dev.tab",
            "data/en-ud-dev.out")
