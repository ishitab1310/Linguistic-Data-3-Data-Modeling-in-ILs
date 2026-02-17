import sys
from src.io_utils import read_tab_sentences, sentence_to_arrays
from src.parser_arc_standard import parse


def main():
    f = open(sys.argv[1], encoding="utf-8")
    sentences = read_tab_sentences(f)

    for sent in sentences:
        words, tags, heads, labels = sentence_to_arrays(sent)
        arcs = parse(words, heads, labels)

        arc_map = {d: (h, l) for h, d, l in arcs}

        for i in range(1, len(words)):
            h, l = arc_map.get(i, (0, "root"))
            print("\t".join([words[i], tags[i], str(h), l]))
        print()


if __name__ == "__main__":
    main()
