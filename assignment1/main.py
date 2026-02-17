# assignment1.py
# Descriptive Linguistic Analysis of Hindi–Urdu Treebank (HUTB)
# Course :Linguistic Data 3: Data Modeling in Indian Languages

import os
from collections import Counter, defaultdict


BASE_PATH = r"F:\00SPRING_2026\LD3\HDTB_PRE_RELEASE_VERSION-0.05\HDTB_pre_release_version-0.05"
DATA_DIRS = [
    os.path.join(BASE_PATH, "IntraChunk", "CoNLL", "utf"),
    os.path.join(BASE_PATH, "InterChunk", "CoNLL", "utf")
]
PUNCT = {"SYM", "PUNCT", "RD_PUNC"}


sent_count, tok_count = 0, 0
sent_lens, vocab = [], set()
pos_freq, case_freq = Counter(), Counter()
unmarked_nouns = 0
word_orders = Counter()
inter_dist, same_case_dist, diff_case_dist = [], [], []




def read_conll(fp):
    sent = []
    with open(fp, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if sent: yield sent; sent = []
            else:
                sent.append(line.split("\t"))
        if sent: yield sent


for base in DATA_DIRS:
    for root, _, files in os.walk(base):
        for fn in files:
           
            if not fn.lower().endswith((".dat")): continue

            for sent in read_conll(os.path.join(root, fn)):

                
                # TASK 1: BASIC STATS
                
                sent_count += 1
                words, cases = [], []
                S = O = V = None

                children = defaultdict(list)
                for c in sent:
                    try:
                        parent = int(c[6])
                        child = int(c[0])
                        children[parent].append(child)
                    except:
                        pass

                for i, c in enumerate(sent):
                    w, pos, feats, dep = c[1], c[3], c[5], c[7]
                    pos_lower = pos.lower()

                    if pos not in PUNCT:
                        words.append(w)
                        tok_count += 1
                        vocab.add(w)
                        pos_freq[pos_lower] += 1

                        # Task 3: unmarked nouns
                        if pos_lower == "psp":
                            case_freq[w] += 1
                            cases.append((w, len(words)))
                        
                        if pos_lower in {"nn", "nnp"}:
                            noun_id = int(c[0])
                            has_psp = False

                            for child_id in children.get(noun_id, []):
                                child = sent[child_id - 1]
                                if child[3].lower() == "psp":
                                    has_psp = True
                                    break

                            if not has_psp:
                                unmarked_nouns += 1

                    # Task 2: identify S,O,V
                    S = i if dep == "k1" else S
                    O = i if dep == "k2" else O
                    V = i if dep == "main" else V

                sent_lens.append(len(words))

                
                # TASK 2: WORD ORDER PATTERNS
                
                if None not in (S, O, V):
                    pattern = "".join(x[1] for x in sorted([(S,"S"),(O,"O"),(V,"V")]))
                    word_orders[pattern] += 1

                
                # TASK 4: INTERVENING DISTANCE
                
                if len(cases) > 1:
                    dists = [abs(p2-p1)-1 for (c1,p1),(c2,p2) in zip(cases, cases[1:])]
                    for (c1,p1),(c2,p2) in zip(cases, cases[1:]):
                        (same_case_dist if c1==c2 else diff_case_dist).append(abs(p2-p1)-1)
                    inter_dist.append(sum(dists)/len(dists) if dists else 0)


# TASK 1: FINAL STATS OUTPUT

print("Total Sentences:", sent_count)
print("Total Tokens:", tok_count)
print("Total Word Types:", len(vocab))
avg_len = sum(sent_lens)/len(sent_lens) if sent_lens else 0
print("Avg Sentence Length:", avg_len)
print("Min Sentence Length:", min(sent_lens) if sent_lens else 0)
print("Max Sentence Length:", max(sent_lens) if sent_lens else 0)


# TASK 2: WORD ORDER

print("\nWord Order Patterns")
for k,v in word_orders.items(): print(k, v)


# TASK 3: CASE & VIBHAKTI

print("\nCase Marker Distribution")
for k,v in case_freq.items(): print(k, v)
print("Unmarked Nouns:", unmarked_nouns)


# TASK 5: POS DISTRIBUTION

print("\nPOS Distribution")
for k,v in pos_freq.items(): print(k, v)


# TASK 4: DISTANCE SUMMARY

avg_inter = sum(inter_dist)/len(inter_dist) if inter_dist else 0
same_avg = sum(same_case_dist)/len(same_case_dist) if same_case_dist else 0
diff_avg = sum(diff_case_dist)/len(diff_case_dist) if diff_case_dist else 0

print("\nAvg Intervening Distance:", avg_inter)
print("Same Case Avg Distance:", same_avg)
print("Different Case Avg Distance:", diff_avg)
