import matplotlib.pyplot as plt
import seaborn as sns


def compute_dependency_distance(df):

    df = df.copy()

    df = df[df["head"] != 0]

    df["distance"] = abs(df["id"] - df["head"])

    return df


def summarize_distances(df, lang):

    mean_dist = df["distance"].mean()
    median_dist = df["distance"].median()

    print(f"\n{lang} Dependency Distance Stats")
    print("Mean:", mean_dist)
    print("Median:", median_dist)

    return mean_dist, median_dist


def plot_histogram(telugu_df, hindi_df):

    plt.figure(figsize=(10,6))

    sns.histplot(telugu_df["distance"], bins=30, label="Telugu", color="blue", stat="density")
    sns.histplot(hindi_df["distance"], bins=30, label="Hindi", color="red", stat="density")

    plt.xlabel("Dependency Distance")
    plt.ylabel("Density")
    plt.title("Dependency Distance Distribution")
    plt.legend()

    plt.savefig("results/dependency_distance_histogram.png")
    plt.close()


def top_dependency_relations(df, lang):

    counts = df["deprel"].value_counts().head(10)

    print(f"\nTop 10 Dependency Relations — {lang}")
    print(counts)

    counts.to_csv(f"results/{lang.lower()}_top_dependencies.csv")

    return counts