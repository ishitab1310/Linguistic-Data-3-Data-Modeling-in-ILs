# Assignment 3: Data Modeling in Indian Languages 

This repository contains the implementation and analysis for **Assignment 3** of Linguistic Data 3. The project focuses on **dependency structure analysis and morphological analysis in parsed linguistic data**.

The project processes dependency-parsed sentences, computes linguistic statistics, and performs statistical testing using **Python and R**. Results include **histograms, statistical summaries, and significance testing**.

---

# Project Structure

```
assignment3/
│
├── results/
│   ├── dependency_distance_histogram.png
│   ├── dependency_statistics.csv
│   └── morphology_statistics.csv
│
│
├── src/
│   ├── dependency_analysis.py
│   ├── morphology_analysis.py
│   ├── parser.py
│   ├── stats_tests.py
│   ├── main.py
│   ├── analysis.R
│   └── test_load.py
│
└── README.md
```

---

# Objective


We:

- Parse dependency tree data
- Compute dependency distance statistics
- Analyze morphological patterns
- Visualize distributions
- Perform statistical testing in R

---

# Requirements

## Python

Python version:
```
Python 3.10
```

Install required packages:

```
pip install pandas matplotlib numpy scipy
```

## R

R version:
```
R 4.0
```

Required packages:

```
install.packages("ggplot2")
```

---

# Running the Python Pipeline

Navigate to the assignment directory:

```
cd assignment3
```

Run the main script:

```
python src/main.py
```

This script will:

1. Load parsed sentences
2. Compute dependency distance statistics
3. Run morphological analysis
4. Save statistics
5. Generate histogram plots

Output files will appear in:

```
results/
```

---



# Output

The following outputs are generated.

## Dependency Distance Histogram

Location:

```
results/dependency_distance_histogram.png
```

This plot shows the distribution of dependency distances across parsed sentences.

## Statistics Tables

Saved as:

```
results/dependency_statistics.csv
results/morphology_statistics.csv
```

These tables contain summary statistics used for further analysis.

---

# Methodology

The pipeline follows these steps:

1. **Dependency Parsing**
   - Load sentences in CoNLL-U format
   - Extract head–dependent relations

2. **Dependency Distance Calculation**
   - Distance = |dependent index − head index|

3. **Morphological Analysis**
   - Extract morphological features
   - Compute feature distributions

4. **Visualization**
   - Plot dependency distance histograms

5. **Statistical Testing**
   - Conduct statistical comparisons using R

---

