import os
import pandas as pd


def read_conll(file_path):

    rows = []

    with open(file_path, encoding="utf8") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 8:
                continue

            try:
                rows.append({
                    "id": int(parts[0]),
                    "form": parts[1],
                    "lemma": parts[2],
                    "upos": parts[3],
                    "xpos": parts[4],
                    "feats": parts[5],
                    "head": int(parts[6]),
                    "deprel": parts[7]
                })
            except:
                continue

    return pd.DataFrame(rows)


def load_telugu_treebank(file_path):

    return read_conll(file_path)


def load_hindi_treebank(folder_path):

    all_rows = []

    for root, _, files in os.walk(folder_path):

        for f in files:

            if f.endswith(".dat"):

                file_path = os.path.join(root, f)

                df = read_conll(file_path)

                all_rows.append(df)

    return pd.concat(all_rows, ignore_index=True)