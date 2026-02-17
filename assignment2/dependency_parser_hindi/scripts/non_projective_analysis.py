"""
Detect non-projective trees in gold data
and estimate parser impact.
"""

def read_sentences(path):
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


def get_arcs(sentence):
    arcs = []
    for i, tok in enumerate(sentence, start=1):
        head = int(tok[2])
        arcs.append((head, i))
    return arcs


def crossing(a, b):
    h1, d1 = a
    h2, d2 = b

    a1, a2 = sorted([h1, d1])
    b1, b2 = sorted([h2, d2])

    return a1 < b1 < a2 < b2


def is_projective(arcs):
    for i in range(len(arcs)):
        for j in range(i + 1, len(arcs)):
            if crossing(arcs[i], arcs[j]):
                return False
    return True


def analyze(path):
    sents = read_sentences(path)

    total = len(sents)
    nonproj = 0

    for sent in sents:
        arcs = get_arcs(sent)
        if not is_projective(arcs):
            nonproj += 1

    print("\n===== NON-PROJECTIVE ANALYSIS =====")
    print(f"Total sentences: {total}")
    print(f"Non-projective sentences: {nonproj}")
    print(f"Percentage: {(nonproj/total)*100:.2f}%")
  


if __name__ == "__main__":
    analyze("data/en-ud-dev.tab")
