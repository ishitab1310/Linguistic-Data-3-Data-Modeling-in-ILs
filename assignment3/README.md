# Assignment 3 — Data Analysis in Psycholinguistics

## Project Structure

```
assignment3/
├── README.md
├── data/
│   ├── hindi/          ← Hindi .dat files (HDTB, IIIT/Paninian format)
│   └── telugu/         ← Telugu .conll file (iiit_hcu_intra_chunk_v1.conll)
├── results/            ← generated plots and CSVs
└── src/
    ├── parser.py               CoNLL/Paninian loader (.dat + .conll)
    ├── dependency_analysis.py  Q1–Q4
    ├── morphology_analysis.py  Q5–Q6
    ├── main.py                 Part 1 runner
    ├── analysis.R              Part 2 (all 9 questions)
    └── report.tex              LaTeX report
```

---

## Treebank Format

Both treebanks use the **IIIT/Paninian annotation scheme** — a 10-column
tab-separated CoNLL format with pipe-separated features using `-` as the
key-value separator:

```
id  form  lemma  coarse_pos  fine_pos  feats  head  deprel  _  _
```

Features example:
```
cat-n|gen-m|num-sg|pers-3|case-o|vib-0_का|tam-0|chunkId-NP|chunkType-head
```

Morphological keys extracted: `cat`, `gen`, `num`, `pers`, `case`, `vib`, `tam`
(chunk metadata keys like `chunkId`, `chunkType`, `stype`, `voicetype` are skipped).

---

## Part 1 — Corpus Analysis (Python)

### Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Data

- Hindi: download HDTB and place `.dat` files in `data/hindi/`
- Telugu: place `iiit_hcu_intra_chunk_v1.conll` in `data/telugu/`

### Run

```bash
cd assignment3
python src/main.py
```

### Outputs

| File | Question |
|------|----------|
| `dependency_distance_histogram.png` | Q1 |
| `dependency_density.png` | Q1 |
| `dependency_boxplot.png` | Q1 |
| `dependency_summary.csv` | Q1, Q4 |
| `dependency_relations_comparison.png` | Q2 |
| `hindi_top_dependencies.csv` | Q2 |
| `telugu_top_dependencies.csv` | Q2 |
| `hindi_morph_features.csv / .png` | Q5 |
| `telugu_morph_features.csv / .png` | Q5 |
| `morph_feature_comparison.csv / .png` | Q5 |
| `morph_feature_heatmap.png` | Q5 |
| `morph_value_gen/case/num/pers.png` | Q5–Q6 |

---

## Part 2 — Experimental Data (R)

### Requirements

```r
install.packages(c("ggplot2", "dplyr", "stringr"))
```

### Data

Download `pset_1_data` from MIT OCW 9.59J:
https://ocw.mit.edu/courses/9-59j-lab-in-psycholinguistics-spring-2017/resources/pset_1_data/

Save as `data/pset_1_data.txt` (tab-separated).

### Run

```bash
Rscript src/analysis.R
# or open in RStudio and source()
```