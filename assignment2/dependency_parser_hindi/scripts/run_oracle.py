import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# ----------------------------------------------------

from src.io_utils import read_tab_sentences, sentence_to_arrays
from src.parser import parse


def main():
    debug = "--debug" in sys.argv

    # input file
    args = [a for a in sys.argv[1:] if a != "--debug"]

    if len(args) > 0:
        f = open(args[0], "r", encoding="utf-8")
    else:
        f = sys.stdin

    sentences = read_tab_sentences(f)

    for sent in sentences:
        words, tags, heads, labels = sentence_to_arrays(sent)

        arcs = parse(words, heads, labels, debug=debug)

        arc_map = {d: (h, l) for h, d, l in arcs}

        for i in range(1, len(words)):
            h, l = arc_map.get(i, (0, "root"))
            print("\t".join([words[i], tags[i], str(h), l]))
        print()


if __name__ == "__main__":
    main()
