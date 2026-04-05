"""
morphology_analysis.py
----------------------
Q5 – Extract and compare morphological features (cat, gen, num, case, pers, tam, vib)
Q6 – Typological discussion data: feature-level comparison table + heatmap

IIIT/Paninian feature format uses '|' between features and '-' as key-value separator:
    cat-n|gen-m|num-sg|pers-3|case-o|vib-0_ka|tam-0|chunkId-NP|...

We keep only linguistic morphological keys and skip chunk/discourse metadata.
Empty values (e.g. gen-  with nothing after the dash) are skipped.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS = "results"
os.makedirs(RESULTS, exist_ok=True)

# Keys that are genuine morphological features (skip chunkId, chunkType, stype, voicetype)
MORPH_KEYS = {"cat", "gen", "num", "pers", "case", "vib", "tam",
              "aspect", "mood", "tense", "voice"}


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def extract_morph_features(df: pd.DataFrame) -> pd.Series:
    """
    Count feature CATEGORY occurrences (e.g. how many tokens have 'gen', 'case', etc.)
    Paninian format: key-value separated by '-', features separated by '|'.
    Empty values (key-) are skipped.
    """
    counts: dict[str, int] = {}

    for cell in df["feats"].dropna():
        for pair in cell.split("|"):
            idx = pair.find("-")
            if idx == -1:
                continue
            key = pair[:idx].strip()
            val = pair[idx+1:].strip()
            # only count if it's a morph key AND has a non-empty value
            if key in MORPH_KEYS and val:
                counts[key] = counts.get(key, 0) + 1

    return pd.Series(counts).sort_values(ascending=False)


def extract_feature_values(df: pd.DataFrame) -> dict[str, pd.Series]:
    """
    For each morphological feature category, count the distribution of values.
    e.g. {'gen': Series({'m': 5000, 'f': 3000, 'any': 200}), ...}
    """
    feat_vals: dict[str, dict[str, int]] = {}

    for cell in df["feats"].dropna():
        for pair in cell.split("|"):
            idx = pair.find("-")
            if idx == -1:
                continue
            key = pair[:idx].strip()
            val = pair[idx+1:].strip()
            if key in MORPH_KEYS and val:
                if key not in feat_vals:
                    feat_vals[key] = {}
                feat_vals[key][val] = feat_vals[key].get(val, 0) + 1

    return {k: pd.Series(v).sort_values(ascending=False) for k, v in feat_vals.items()}


# ---------------------------------------------------------------------------
# Q5 – Plots
# ---------------------------------------------------------------------------

def plot_feature_bar(feat_series: pd.Series, lang: str):
    fig, ax = plt.subplots(figsize=(10, 6))
    color = "#2196F3" if lang == "Telugu" else "#F44336"
    feat_series.plot(kind="bar", ax=ax, color=color, alpha=0.85)
    ax.set_xlabel("Feature Category", fontsize=12)
    ax.set_ylabel("Token Count", fontsize=12)
    ax.set_title(f"Morphological Features — {lang}", fontsize=14)
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    path = os.path.join(RESULTS, f"{lang.lower()}_morph_features.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


def plot_feature_comparison(telugu_feats: pd.Series, hindi_feats: pd.Series):
    all_keys = list(dict.fromkeys(list(telugu_feats.index) + list(hindi_feats.index)))
    t_vals = [telugu_feats.get(k, 0) for k in all_keys]
    h_vals = [hindi_feats.get(k, 0) for k in all_keys]

    x = np.arange(len(all_keys))
    width = 0.38
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - width/2, t_vals, width, label="Telugu", color="#2196F3", alpha=0.85)
    ax.bar(x + width/2, h_vals, width, label="Hindi",  color="#F44336", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(all_keys, rotation=30, ha="right", fontsize=11)
    ax.set_ylabel("Token Count", fontsize=12)
    ax.set_title("Morphological Feature Comparison: Hindi vs Telugu", fontsize=14)
    ax.legend(fontsize=11)
    plt.tight_layout()
    path = os.path.join(RESULTS, "morph_feature_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


def save_feature_tables(telugu_feats: pd.Series, hindi_feats: pd.Series) -> pd.DataFrame:
    for feats, lang in [(telugu_feats, "telugu"), (hindi_feats, "hindi")]:
        df = feats.reset_index()
        df.columns = ["feature", "count"]
        path = os.path.join(RESULTS, f"{lang}_morph_features.csv")
        df.to_csv(path, index=False)
        print(f"[csv] Saved → {path}")

    merged = pd.DataFrame({"Telugu": telugu_feats, "Hindi": hindi_feats}).fillna(0).astype(int)
    merged.index.name = "Feature"
    merged["Total"] = merged["Telugu"] + merged["Hindi"]
    merged = merged.sort_values("Total", ascending=False)
    path = os.path.join(RESULTS, "morph_feature_comparison.csv")
    merged.reset_index().to_csv(path, index=False)
    print(f"[csv] Saved → {path}")
    return merged


def plot_heatmap(merged_df: pd.DataFrame):
    top = merged_df.drop(columns="Total").copy()
    top_norm = top.div(top.sum(axis=0), axis=1) * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(top_norm, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.5, ax=ax,
                cbar_kws={"label": "% of feature tokens"})
    ax.set_title("Normalised Morphological Feature Frequencies (%)", fontsize=13)
    plt.tight_layout()
    path = os.path.join(RESULTS, "morph_feature_heatmap.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


# ---------------------------------------------------------------------------
# Value-level plots for key features (gen, case, num)
# ---------------------------------------------------------------------------

def plot_value_distribution(t_vals: dict, h_vals: dict, feature: str):
    """Bar chart comparing value distributions for a single feature."""
    t_s = t_vals.get(feature, pd.Series(dtype=int))
    h_s = h_vals.get(feature, pd.Series(dtype=int))

    all_vals = list(dict.fromkeys(list(t_s.index) + list(h_s.index)))
    if not all_vals:
        return

    x = np.arange(len(all_vals))
    width = 0.38
    fig, ax = plt.subplots(figsize=(max(8, len(all_vals)), 5))
    ax.bar(x - width/2, [t_s.get(v, 0) for v in all_vals], width,
           label="Telugu", color="#2196F3", alpha=0.85)
    ax.bar(x + width/2, [h_s.get(v, 0) for v in all_vals], width,
           label="Hindi", color="#F44336", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(all_vals, rotation=30, ha="right")
    ax.set_ylabel("Count")
    ax.set_title(f"Feature '{feature}' Value Distribution: Hindi vs Telugu")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(RESULTS, f"morph_value_{feature}.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_all(telugu_raw: pd.DataFrame, hindi_raw: pd.DataFrame):
    print("\n" + "="*40)
    print("Morphological Feature Analysis")
    print("="*40)

    telugu_feats = extract_morph_features(telugu_raw)
    hindi_feats  = extract_morph_features(hindi_raw)

    print("\nTop Telugu Features:")
    print(telugu_feats.to_string())
    print("\nTop Hindi Features:")
    print(hindi_feats.to_string())

    plot_feature_bar(telugu_feats, "Telugu")
    plot_feature_bar(hindi_feats,  "Hindi")
    plot_feature_comparison(telugu_feats, hindi_feats)
    merged = save_feature_tables(telugu_feats, hindi_feats)
    plot_heatmap(merged)

    # value-level breakdown for key features
    t_vals = extract_feature_values(telugu_raw)
    h_vals = extract_feature_values(hindi_raw)
    for feat in ["gen", "case", "num", "pers"]:
        plot_value_distribution(t_vals, h_vals, feat)

    return {
        "telugu_feats": telugu_feats,
        "hindi_feats":  hindi_feats,
        "telugu_vals":  t_vals,
        "hindi_vals":   h_vals,
        "merged":       merged,
    }