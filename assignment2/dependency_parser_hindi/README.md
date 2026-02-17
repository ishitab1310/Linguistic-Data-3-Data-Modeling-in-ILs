# Hindi Dependency Parser (Transition-Based Parsing)

This project implements a transition-based dependency parser for Hindi using Python.

## Implemented Components

### 1. Arc-Eager Transition System
Implemented parser actions:

- SH (Shift)
- RE (Reduce)
- RA (Right Arc)
- LA (Left Arc)

The parser configuration includes:

- Stack
- Buffer
- Arc set

The implementation follows Chapter 3 of Kübler et al.



### 2. Static Oracle

A static oracle was implemented based on Goldberg & Nivre (2012).

Oracle decisions:

- LEFT-ARC if buffer word is head of stack word
- RIGHT-ARC if stack word is head of buffer word
- REDUCE when stack token is complete
- otherwise SHIFT

---

### 3. Testing and Evaluation

Implemented evaluation on:

- Example sentence (`example.tab`)
- Development treebank (`en-ud-dev.tab`)
- Hindi HUTB corpus (.dat files)

Scripts include:

- debug parser output
- error analysis
- non-projective sentence analysis

---

### 4. Extra Credit

Implemented:

- Arc-Standard transition system
- Projectivization algorithm for dependency trees

---

## Running the Parser

### Example sentence

```bash
python -m scripts.run_oracle data/example.tab
```
#### Debug mode
```bash
python -m scripts.run_oracle data/example.tab --debug
```

#### Development set
```bash
python -m scripts.run_oracle data/en-ud-dev.tab
```
#### Parse HUTB dataset
```bash
python -m scripts.run_hutb_dev
```
## Project Structure
```bash
src/        # parser implementation
scripts/    # scripts to run
data/       # datasets
starter/     # starter code
```