from scipy.stats import ttest_ind


def dependency_distance_ttest(telugu_df, hindi_df):

    t_stat, p_val = ttest_ind(
        telugu_df["distance"],
        hindi_df["distance"],
        equal_var=False
    )

    print("\nDependency Distance T-Test")

    print("t-statistic:", t_stat)
    print("p-value:", p_val)

    if p_val < 0.05:
        print("Result: Significant difference (p < 0.05)")
    else:
        print("Result: Not significant (p >= 0.05)")