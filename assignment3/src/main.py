from parser import load_telugu_treebank, load_hindi_treebank
from dependency_analysis import (
    compute_dependency_distance,
    summarize_distances,
    plot_histogram,
    top_dependency_relations
)
from morphology_analysis import compare_features
from stats_tests import dependency_distance_ttest


print("Loading Telugu treebank...")
telugu = load_telugu_treebank("data/telugu/iiit_hcu_intra_chunk_v1.conll")

print("Loading Hindi treebank...")
hindi = load_hindi_treebank("data/hindi")

print("\nTelugu tokens:", len(telugu))
print("Hindi tokens:", len(hindi))


# Dependency distance
telugu_dist = compute_dependency_distance(telugu)
hindi_dist = compute_dependency_distance(hindi)


summarize_distances(telugu_dist, "Telugu")
summarize_distances(hindi_dist, "Hindi")


plot_histogram(telugu_dist, hindi_dist)


# Top dependency relations
top_dependency_relations(telugu, "Telugu")
top_dependency_relations(hindi, "Hindi")


# Significance testing
dependency_distance_ttest(telugu_dist, hindi_dist)


# Morphological comparison
compare_features(telugu, hindi)