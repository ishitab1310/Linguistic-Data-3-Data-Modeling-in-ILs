"""
main.py
-------
Run from the project root (assignment3/):

    python src/main.py

Assumes treebanks are at:
    data/hindi/   -- .dat files
    data/telugu/  -- .conll files
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from parser              import load_treebank
from dependency_analysis import run_all as run_dependency
from morphology_analysis import run_all as run_morphology


HINDI_DIR  = os.path.join("data", "hindi")
TELUGU_DIR = os.path.join("data", "telugu")


def main():
    os.makedirs("results", exist_ok=True)

    print("\n[main] Loading treebanks …")
    hindi  = load_treebank(HINDI_DIR,  lang="Hindi",  extensions=(".dat",))
    telugu = load_treebank(TELUGU_DIR, lang="Telugu", extensions=(".conll",))

    print("\n[main] Running dependency analysis (Q1–Q4) …")
    dep = run_dependency(telugu, hindi)

    print("\n[main] Running morphology analysis (Q5–Q6) …")
    morph = run_morphology(telugu, hindi)

    print("\n" + "="*50)
    print("Done. All outputs in results/")
    print("="*50)
    sig = dep["sig"]
    print(f"  Telugu mean dep dist : {dep['telugu_stats']['mean']}")
    print(f"  Hindi  mean dep dist : {dep['hindi_stats']['mean']}")
    print(f"  Mann-Whitney U p     : {sig['p_value']:.4e}  significant={sig['significant']}")


if __name__ == "__main__":
    main()