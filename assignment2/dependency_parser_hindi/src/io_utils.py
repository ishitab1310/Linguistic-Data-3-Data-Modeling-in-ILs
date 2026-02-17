# src/io_utils.py

def read_tab_sentences(file_obj):
    """
    Reads both:
    1) assignment example.tab format
    2) HUTB .dat CoNLL format
    """

    sentences = []
    sent = []

    for line in file_obj:
        line = line.strip()

        if not line:
            if sent:
                sentences.append(sent)
            sent = []
            continue

        if line.startswith("#"):
            continue

        sent.append(line.split("\t"))

    if sent:
        sentences.append(sent)

    return sentences


def sentence_to_arrays(sentence):
    """
    Automatically detects input format.
    Returns:
        words, tags, heads, labels
    """

    # root token
    words = ["root"]
    tags = ["_"]
    heads = [0]
    labels = ["root"]

    
    hutb_format = len(sentence[0]) >= 8

    for tok in sentence:

        if hutb_format:
            # HUTB CoNLL 
            word = tok[1]
            tag = tok[4]
            head = int(tok[6])
            label = tok[7]

        else:
            # assignment tab 
            word = tok[0]
            tag = tok[1]
            head = int(tok[2])
            label = tok[3]

        words.append(word)
        tags.append(tag)
        heads.append(head)
        labels.append(label)

    return words, tags, heads, labels
