import pandas as pd
import matplotlib.pyplot as plt


def extract_morph_features(df):

    features = {}

    for feats in df["feats"].dropna():

        parts = feats.split("|")

        for p in parts:

            if "-" in p:

                key, _ = p.split("-",1)

                if key not in features:
                    features[key] = 0

                features[key] += 1

    return pd.Series(features).sort_values(ascending=False)


def compare_features(telugu, hindi):

    telugu_feats = extract_morph_features(telugu)
    hindi_feats = extract_morph_features(hindi)

    print("\nTop Telugu Morphological Features")
    print(telugu_feats.head(10))

    print("\nTop Hindi Morphological Features")
    print(hindi_feats.head(10))

    telugu_feats.to_csv("results/telugu_morph_features.csv")
    hindi_feats.to_csv("results/hindi_morph_features.csv")

    plt.figure(figsize=(10,6))

    telugu_feats.head(10).plot(kind="bar", title="Top Telugu Morph Features")

    plt.savefig("results/telugu_morph_features.png")
    plt.close()

    plt.figure(figsize=(10,6))

    hindi_feats.head(10).plot(kind="bar", title="Top Hindi Morph Features")

    plt.savefig("results/hindi_morph_features.png")
    plt.close()