# Case Marking and Word Order Analysis in Hindi–Urdu

## Overview
This project presents a corpus-based analysis of word order, case marking, and syntactic patterns in Hindi–Urdu using the Hindi–Urdu Treebank (HUTB) pre-release version 0.05. The study leverages dependency annotations to examine noun–verb order, postpositional case marking, intervening distances between case markers, and part-of-speech distributions.

The analysis was implemented as part of an ANLP assignment and goes beyond the basic requirements by incorporating dependency-based case identification and detailed corpus statistics.

---

## Dataset
The study uses the **Hindi–Urdu Treebank (HUTB) pre-release v0.05**.

All dependency-annotated files in **CoNLL format** were used from both:
- **IntraChunk**
- **InterChunk**

The following domains and splits were included:

IntraChunk/CoNLL/utf/
InterChunk/CoNLL/utf/
├── conversation
├── news_articles_and_heritage
├── Training
├── Development
└── Testing


### Why only CoNLL + utf?
- **CoNLL** → provides dependency relations (k1, k2, main, etc.)
- **utf** → readable Hindi text

Punctuation tokens were excluded where specified.

---

## Methodology

### Word Order Analysis
- SOV, SVO, VSO patterns were identified using dependency relations.
- The position of the main verb relative to its core arguments was computed.

### Case Marker Analysis
In the Hindi–Urdu Treebank, case marking is primarily realized through **postpositions (tagged as PSP)** rather than morphological `Case=` features on nouns. Therefore:
- Case markers were identified using postposition tokens.
- A noun was classified as **unmarked** if it did not govern a dependent PSP in the dependency tree.

### Intervening Distance
- Average distance between successive case markers was computed.
- Distances between same vs. different postpositions were compared to observe clustering behavior.

### POS Distribution
- Universal POS tags were counted across the corpus.
- Noun–verb distribution was analyzed to characterize syntactic tendencies.

---

## Key Results
- **SOV** emerged as the dominant word order.
- Postpositions such as **के, में, की, को, से, ने** were the most frequent case markers.
- A small number of nouns were found to be **unmarked**, identified through dependency structure.
- Same case markers tend to occur farther apart than different case markers.
- Nouns outnumber verbs, reflecting the nominal richness of Hindi–Urdu.

---

## Files
- `main.py` – main analysis script
- `results.txt` – output statistics
- `report.pdf` – detailed assignment report
- `README.md` – project documentation

---

## Requirements
- Python 3.x
- Standard Python libraries (`os`, `collections`, `statistics`)

---

## How to Run
```bash
python main.py