"""
dependency_analysis.py
----------------------
Q1 – Dependency distance distribution (histogram, mean, median)
Q2 – Top-10 dependency relations comparison
Q3 – Discussed in report; data produced here
Q4 – Significance testing (Mann-Whitney U) for distance differences
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

RESULTS = "results"
os.makedirs(RESULTS, exist_ok=True)

# ---------------------------------------------------------------------------
# Q1 helpers
# ---------------------------------------------------------------------------

def compute_dependency_distance(df: pd.DataFrame) -> pd.DataFrame:
    """Add 'distance' column; drop root tokens (head == 0)."""
    df = df.copy()
    df = df[df["head"].notna() & (df["head"] != 0)]
    df["distance"] = (df["id"] - df["head"]).abs()
    return df


def summarize_distances(df: pd.DataFrame, lang: str) -> dict:
    """Print and return basic distance statistics."""
    d = df["distance"]
    stats_dict = {
        "language": lang,
        "mean":     round(d.mean(), 4),
        "median":   d.median(),
        "std":      round(d.std(), 4),
        "min":      int(d.min()),
        "max":      int(d.max()),
        "n":        len(d),
    }
    print(f"\n{'='*40}")
    print(f"{lang} Dependency Distance Statistics")
    print(f"{'='*40}")
    for k, v in stats_dict.items():
        print(f"  {k:<10}: {v}")
    return stats_dict


def plot_histogram(telugu_df: pd.DataFrame, hindi_df: pd.DataFrame):
    """Q1 – Overlapping density histogram of dependency distances."""
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(telugu_df["distance"], bins=30, label="Telugu",
                 color="#2196F3", stat="density", alpha=0.6, ax=ax)
    sns.histplot(hindi_df["distance"],  bins=30, label="Hindi",
                 color="#F44336", stat="density", alpha=0.6, ax=ax)

    ax.set_xlabel("Dependency Distance (|head − dependent|)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Dependency Distance Distribution: Hindi vs Telugu", fontsize=14)
    ax.legend(fontsize=11)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.tight_layout()
    path = os.path.join(RESULTS, "dependency_distance_histogram.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


def plot_density(telugu_df: pd.DataFrame, hindi_df: pd.DataFrame):
    """KDE density curves for dependency distances."""
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.kdeplot(telugu_df["distance"], label="Telugu", color="#2196F3",
                fill=True, alpha=0.35, ax=ax)
    sns.kdeplot(hindi_df["distance"],  label="Hindi",  color="#F44336",
                fill=True, alpha=0.35, ax=ax)

    ax.set_xlabel("Dependency Distance", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("KDE of Dependency Distances: Hindi vs Telugu", fontsize=14)
    ax.legend(fontsize=11)

    plt.tight_layout()
    path = os.path.join(RESULTS, "dependency_density.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


def plot_boxplot(telugu_df: pd.DataFrame, hindi_df: pd.DataFrame):
    """Side-by-side boxplot of dependency distances."""
    combined = pd.concat([
        telugu_df[["distance"]].assign(Language="Telugu"),
        hindi_df[["distance"]].assign(Language="Hindi"),
    ])

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=combined, x="Language", y="distance",
                palette={"Telugu": "#2196F3", "Hindi": "#F44336"}, ax=ax)

    ax.set_ylabel("Dependency Distance", fontsize=12)
    ax.set_title("Boxplot of Dependency Distances: Hindi vs Telugu", fontsize=14)

    plt.tight_layout()
    path = os.path.join(RESULTS, "dependency_boxplot.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


# ---------------------------------------------------------------------------
# Q2 helpers
# ---------------------------------------------------------------------------

def top_dependency_relations(df: pd.DataFrame, lang: str) -> pd.Series:
    """Return top-10 deprels and save to CSV."""
    counts = df["deprel"].dropna().value_counts().head(10)

    print(f"\nTop 10 Dependency Relations — {lang}")
    print(counts.to_string())

    out_path = os.path.join(RESULTS, f"{lang.lower()}_top_dependencies.csv")
    counts.reset_index().rename(columns={"index": "deprel", "deprel": "count"}).to_csv(
        out_path, index=False
    )
    print(f"[csv] Saved → {out_path}")
    return counts


def plot_dependency_relations(telugu_counts: pd.Series, hindi_counts: pd.Series):
    """Grouped bar chart comparing top-10 deprels for both languages."""
    # merge on relation label; fill missing with 0
    merged = pd.DataFrame({
        "Telugu": telugu_counts,
        "Hindi":  hindi_counts,
    }).fillna(0)

    merged = merged.sort_values("Telugu", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(merged))
    width = 0.38

    ax.bar(x - width/2, merged["Telugu"], width, label="Telugu", color="#2196F3", alpha=0.85)
    ax.bar(x + width/2, merged["Hindi"],  width, label="Hindi",  color="#F44336", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(merged.index, rotation=35, ha="right", fontsize=10)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title("Top Dependency Relations: Hindi vs Telugu", fontsize=14)
    ax.legend(fontsize=11)

    plt.tight_layout()
    path = os.path.join(RESULTS, "dependency_relations_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[plot] Saved → {path}")


# ---------------------------------------------------------------------------
# Q4 – Significance testing
# ---------------------------------------------------------------------------

def significance_test(telugu_df: pd.DataFrame, hindi_df: pd.DataFrame) -> dict:
    """
    Mann-Whitney U test (non-parametric) comparing dependency distance
    distributions.  Also computes Cohen's d as effect size.
    """
    t_dist = telugu_df["distance"].dropna().values
    h_dist = hindi_df["distance"].dropna().values

    u_stat, p_value = stats.mannwhitneyu(t_dist, h_dist, alternative="two-sided")

    # Cohen's d
    pooled_std = np.sqrt((t_dist.std()**2 + h_dist.std()**2) / 2)
    cohens_d   = (t_dist.mean() - h_dist.mean()) / pooled_std if pooled_std else float("nan")

    result = {
        "test":       "Mann-Whitney U",
        "U_statistic": round(float(u_stat), 2),
        "p_value":     float(p_value),
        "significant": p_value < 0.05,
        "telugu_mean": round(float(t_dist.mean()), 4),
        "hindi_mean":  round(float(h_dist.mean()), 4),
        "cohens_d":    round(float(cohens_d), 4),
    }

    print("\n" + "="*40)
    print("Significance Test: Dependency Distance")
    print("="*40)
    for k, v in result.items():
        print(f"  {k:<16}: {v}")

    return result


# ---------------------------------------------------------------------------
# Summary CSV
# ---------------------------------------------------------------------------

def save_summary(telugu_stats: dict, hindi_stats: dict, sig: dict):
    rows = [telugu_stats, hindi_stats]
    df = pd.DataFrame(rows)
    df["U_statistic"] = sig["U_statistic"]
    df["p_value"]     = sig["p_value"]
    df["significant"] = sig["significant"]
    df["cohens_d"]    = sig["cohens_d"]
    path = os.path.join(RESULTS, "dependency_summary.csv")
    df.to_csv(path, index=False)
    print(f"[csv] Saved → {path}")


# ---------------------------------------------------------------------------
# Run all Q1-Q4 analyses
# ---------------------------------------------------------------------------

def run_all(telugu_raw: pd.DataFrame, hindi_raw: pd.DataFrame):
    """
    Entry point called from main.py.

    Parameters
    ----------
    telugu_raw, hindi_raw : pd.DataFrame
        Raw token DataFrames from parser.load_treebank().
    """
    # compute distances
    telugu_dist = compute_dependency_distance(telugu_raw)
    hindi_dist  = compute_dependency_distance(hindi_raw)

    # Q1
    t_stats = summarize_distances(telugu_dist, "Telugu")
    h_stats = summarize_distances(hindi_dist,  "Hindi")
    plot_histogram(telugu_dist, hindi_dist)
    plot_density(telugu_dist, hindi_dist)
    plot_boxplot(telugu_dist, hindi_dist)

    # Q2
    t_counts = top_dependency_relations(telugu_dist, "Telugu")
    h_counts = top_dependency_relations(hindi_dist,  "Hindi")
    plot_dependency_relations(t_counts, h_counts)

    # Q4 – significance
    sig = significance_test(telugu_dist, hindi_dist)

    # save summary
    save_summary(t_stats, h_stats, sig)

    return {
        "telugu_dist": telugu_dist,
        "hindi_dist":  hindi_dist,
        "telugu_stats": t_stats,
        "hindi_stats":  h_stats,
        "sig":          sig,
        "telugu_counts": t_counts,
        "hindi_counts":  h_counts,
    }
