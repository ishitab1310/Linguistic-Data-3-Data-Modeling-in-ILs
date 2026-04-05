"""
parser.py
---------
Loads IIIT/Paninian dependency treebanks (Hindi .dat and Telugu .conll).

Format: 10-column tab-separated CoNLL with Paninian annotation.
Columns: id  form  lemma  coarse_pos  fine_pos  feats  head  deprel  _  _

Features field uses pipe-separated key-value pairs with '-' as separator:
    cat-n|gen-m|num-sg|pers-3|case-o|vib-0_ka|tam-0|chunkId-NP|...

Sentences are separated by blank lines.
"""

import os
import re
import pandas as pd


def _parse_id(val: str):
    if re.fullmatch(r"\d+", val):
        return int(val)
    return None


def _parse_head(val: str):
    if re.fullmatch(r"\d+", val):
        return int(val)
    return None


def parse_file(path: str, lang: str = "") -> pd.DataFrame:
    rows = []
    sent_id = 0

    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")

            if line == "":
                sent_id += 1
                continue

            if line.startswith("#"):
                continue

            parts = line.split("\t")
            if len(parts) < 8:
                continue

            tok_id = _parse_id(parts[0])
            if tok_id is None:
                continue

            head = _parse_head(parts[6])
            feats_raw = parts[5] if parts[5] != "_" else None

            row = {
                "sent_id":    sent_id,
                "id":         tok_id,
                "form":       parts[1],
                "lemma":      parts[2],
                "coarse_pos": parts[3],
                "fine_pos":   parts[4],
                "feats":      feats_raw,
                "head":       head,
                "deprel":     parts[7] if parts[7] != "_" else None,
                "lang":       lang,
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    for col in ("id", "head"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_treebank(root: str, lang: str,
                  extensions=(".dat", ".conll", ".conllu", ".conll06")) -> pd.DataFrame:
    """
    Recursively load all treebank files under root.
    """
    frames = []

    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if any(fname.endswith(ext) for ext in extensions):
                fpath = os.path.join(dirpath, fname)
                try:
                    df = parse_file(fpath, lang=lang)
                    if not df.empty:
                        frames.append(df)
                except Exception as exc:
                    print(f"[parser] Warning: could not parse {fpath}: {exc}")

    if not frames:
        raise FileNotFoundError(
            f"No treebank files found under '{root}' with extensions {extensions}."
        )

    combined = pd.concat(frames, ignore_index=True)
    print(f"[parser] Loaded {lang}: {len(combined):,} tokens from {len(frames)} file(s).")
    return combined