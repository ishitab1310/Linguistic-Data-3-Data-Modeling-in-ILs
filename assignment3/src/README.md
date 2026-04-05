# Assignment 3 — Data Analysis in Psycholinguistics

## Structure

```
assignment3/
├── README.md
├── LD3_a3.pdf                  ← assignment brief
├── data/                       ← treebank data (downloaded separately, not committed)
│   ├── telugu_treebank/
│   ├── hindi_treebank/
│   └── pset_1_data.txt
├── results/                    ← all generated plots and CSVs
└── src/
    ├── parser.py               ← CoNLL-U / CoNLL-2006 loader
    ├── dependency_analysis.py  ← Q1–Q4 (dep distances, relations, significance)
    ├── morphology_analysis.py  ← Q5–Q6 (morphological features)
    ├── main.py                 ← orchestrates Part 1
    └── analysis.R              ← Part 2 (all 9 questions, R / ggplot2)
```

---

## Part 1 — Corpus Analysis (Python)

### Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Data setup

1. **Telugu treebank** — clone from GitHub:
   ```bash
   git clone https://github.com/ltrc/telugu_treebank data/telugu_treebank
   ```

2. **Hindi treebank** — download and unzip:
   ```bash
   wget https://ltrc.iiit.ac.in/treebank_H2014/HDTB_pre_release_version-0.05.zip
   unzip HDTB_pre_release_version-0.05.zip -d data/hindi_treebank
   ```

### Run

```bash
cd assignment3
python src/main.py \
    --telugu data/telugu_treebank \
    --hindi  data/hindi_treebank
```

All plots and CSVs will be saved to `results/`.

### Output files (Part 1)

| File | Content | Question |
|------|---------|----------|
| `dependency_distance_histogram.png` | Overlapping density histogram | Q1 |
| `dependency_density.png` | KDE curves | Q1 |
| `dependency_boxplot.png` | Side-by-side boxplots | Q1 |
| `dependency_summary.csv` | Mean, median, std, significance test | Q1, Q4 |
| `telugu_top_dependencies.csv` | Top-10 deprels Telugu | Q2 |
| `hindi_top_dependencies.csv` | Top-10 deprels Hindi | Q2 |
| `dependency_relations_comparison.png` | Grouped bar chart deprels | Q2 |
| `telugu_morph_features.csv` | Feature counts Telugu | Q5 |
| `hindi_morph_features.csv` | Feature counts Hindi | Q5 |
| `morph_feature_comparison.csv` | Side-by-side feature table | Q5 |
| `telugu_morph_features.png` | Bar chart Telugu features | Q5 |
| `hindi_morph_features.png` | Bar chart Hindi features | Q5 |
| `morph_feature_comparison.png` | Grouped comparison bar chart | Q5 |
| `morph_feature_heatmap.png` | Normalised heatmap | Q5 |

---

## Part 2 — Experimental Data (R)

### Requirements

```r
install.packages(c("ggplot2", "dplyr", "stringr"))
```

### Data setup

Download `pset_1_data.txt` from:
> https://ocw.mit.edu/courses/9-59j-lab-in-psycholinguistics-spring-2017/resources/pset_1_data/

Save it as `data/pset_1_data.txt`.

### Run

```bash
Rscript src/analysis.R
```

Or open `src/analysis.R` in RStudio and source it.

### Output files (Part 2)

| File | Content | Question |
|------|---------|----------|
| `Q1_rt_histogram_all.png` | RT histogram all subjects | Q1 |
| `Q2_rt_histogram_faceted.png` | RT histograms by age group | Q2 |
| `Q3_high_z_words.csv` | Words with z-score > 3 | Q3 |
| `Q4_nounfreq_distribution.png` | NounFrequency distribution | Q4 |
| `Q6_boxplot_noun_verb.png` | Boxplot noun vs verb RT | Q6 |
| `Q7_barplot_ci_noun_verb.png` | Bar plot with 95% CI | Q7 |
| `Q8_boxplot_by_letter.png` | Boxplot RT by initial letter | Q8 |
| `Q9_boxplot_two_consonants.png` | Two-consonant vs other RT | Q9 |

---

## Notes

- The CoNLL-U morphological features use `=` as the key-value separator (e.g. `Number=Sing`), not `-`.
- The parser handles both 10-column CoNLL-U and 8-column CoNLL-2006 files.
- Significance testing for dependency distances uses the Mann-Whitney U test (non-parametric, appropriate for skewed count data).
- All R plots use `ggplot2`; all Python plots use `matplotlib` / `seaborn`.
