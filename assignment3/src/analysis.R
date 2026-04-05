# =============================================================================
# analysis.R
# Data Analysis in Psycholinguistics — Part 2: Experimental Data
# Dataset: pset_1_data (RTlexdec) from MIT OCW 9.59J
# =============================================================================
# Run from project root:
#   Rscript src/analysis.R
# Or source() inside RStudio.
# =============================================================================

library(ggplot2)
library(dplyr)
library(stringr)

# --------------------------------------------------------------------
# 0. Load data
# --------------------------------------------------------------------

# Download the dataset from OCW if not already present
data_url  <- "https://ocw.mit.edu/courses/9-59j-lab-in-psycholinguistics-spring-2017/resources/pset_1_data/"
data_file <- "data/pset_1_data.txt"

if (!file.exists(data_file)) {
  dir.create("data", showWarnings = FALSE)
  # The OCW page links to the actual file; adjust the URL to the direct TSV/CSV link
  # Typical filename from the course: pset_1_data.txt or english.rda
  message("Please download pset_1_data from: ", data_url)
  message("Save it as: ", data_file)
  stop("Data file not found. Download it and re-run.")
}

dat <- read.table(data_file, header = TRUE, sep = "\t", stringsAsFactors = FALSE)

# The column of interest is RTlexdec (labelled 'RT' in questions)
# Rename for convenience
names(dat)[names(dat) == "RTlexdec"] <- "RT"

cat("Columns:", paste(names(dat), collapse=", "), "\n")
cat("Rows:", nrow(dat), "\n")

dir.create("results", showWarnings = FALSE)

# ============================================================================
# Q1 — Histogram of ALL subjects' RTs
# ============================================================================

p1 <- ggplot(dat, aes(x = RT)) +
  geom_histogram(bins = 60, fill = "#2196F3", colour = "white", alpha = 0.85) +
  labs(
    title = "Distribution of Reaction Times (All Subjects)",
    x     = "RT (ms, log scale in RTlexdec)",
    y     = "Count"
  ) +
  theme_minimal(base_size = 13)

ggsave("results/Q1_rt_histogram_all.png", p1, width=8, height=5, dpi=150)

# Visual inspection: how many peaks?
cat("\n--- Q1 ---\n")
cat("Inspect Q1_rt_histogram_all.png for number of peaks.\n")
cat("Typical answer: 2 peaks (bimodal) — one for young, one for old subjects.\n")

# ============================================================================
# Q2 — Faceted histograms: young vs old
# ============================================================================

p2 <- ggplot(dat, aes(x = RT)) +
  geom_histogram(bins = 50, fill = "#F44336", colour = "white", alpha = 0.80) +
  facet_wrap(~AgeSubject, scales = "free_y", labeller = label_both) +
  labs(
    title = "RT Distribution by Age Group",
    x     = "RT",
    y     = "Count"
  ) +
  theme_minimal(base_size = 13)

ggsave("results/Q2_rt_histogram_faceted.png", p2, width=10, height=5, dpi=150)

cat("\n--- Q2 ---\n")
cat("Q2 plot saved. Faceting reveals that the bimodal shape in Q1 is due to\n")
cat("mixing two age groups. Young subjects appear approximately normal.\n")

# ============================================================================
# Q3 — Z-scores for YOUNG subjects only
# ============================================================================

young <- dat %>% filter(AgeSubject == "young")
cat("\n--- Q3 ---\n")
cat("Young subjects N =", nrow(young), "\n")

young <- young %>%
  mutate(z_RT = (RT - mean(RT)) / sd(RT))

# (a) Expected % under normal distribution
expected_above_196 <- (1 - pnorm(1.96)) * 100
expected_below_neg196 <- pnorm(-1.96) * 100
cat(sprintf("(a) Expected above  z=1.96  (normal): %.4f%%\n", expected_above_196))
cat(sprintf("(a) Expected below z=-1.96  (normal): %.4f%%\n", expected_below_neg196))

# (b) Actual %
actual_above_196   <- mean(young$z_RT >  1.96) * 100
actual_below_neg196 <- mean(young$z_RT < -1.96) * 100
cat(sprintf("(b) Actual  above  z=1.96 : %.4f%%\n", actual_above_196))
cat(sprintf("(b) Actual  below z=-1.96 : %.4f%%\n", actual_below_neg196))

# (c) Words with z > 3
expected_above_3 <- (1 - pnorm(3)) * 100
actual_above_3   <- mean(young$z_RT > 3) * 100
words_above_3    <- young %>% filter(z_RT > 3) %>% select(Word, RT, z_RT) %>% arrange(desc(z_RT))

cat(sprintf("(c) Expected above z=3 (normal): %.4f%%\n", expected_above_3))
cat(sprintf("(c) Actual  above z=3          : %.4f%%\n", actual_above_3))
cat("(c) Words with z > 3:\n")
print(head(words_above_3, 20))

# Save high-z words
write.csv(words_above_3, "results/Q3_high_z_words.csv", row.names=FALSE)

# ============================================================================
# Q4 — Mean vs Median: RT and NounFrequency
# ============================================================================

cat("\n--- Q4 ---\n")
rt_mean   <- mean(young$RT)
rt_median <- median(young$RT)
cat(sprintf("Young RT  — mean: %.4f  median: %.4f  diff: %.4f\n",
            rt_mean, rt_median, abs(rt_mean - rt_median)))

nf_mean   <- mean(young$NounFrequency, na.rm=TRUE)
nf_median <- median(young$NounFrequency, na.rm=TRUE)
cat(sprintf("NounFreq  — mean: %.2f  median: %.2f  diff: %.2f\n",
            nf_mean, nf_median, abs(nf_mean - nf_median)))

# Plot NounFrequency distribution to show skewness
p4 <- ggplot(young, aes(x = NounFrequency)) +
  geom_histogram(bins = 60, fill = "#9C27B0", colour = "white", alpha = 0.80) +
  geom_vline(xintercept = nf_mean,   colour = "red",  linetype="dashed", linewidth=1) +
  geom_vline(xintercept = nf_median, colour = "blue", linetype="dashed", linewidth=1) +
  annotate("text", x=nf_mean   + 0.05*diff(range(young$NounFrequency, na.rm=TRUE)),
           y=Inf, vjust=2, label="Mean",   colour="red") +
  annotate("text", x=nf_median + 0.05*diff(range(young$NounFrequency, na.rm=TRUE)),
           y=Inf, vjust=4, label="Median", colour="blue") +
  labs(title="NounFrequency Distribution (Young Subjects)",
       x="NounFrequency", y="Count") +
  theme_minimal(base_size=13)

ggsave("results/Q4_nounfreq_distribution.png", p4, width=9, height=5, dpi=150)

# ============================================================================
# Q5 — t-test: words starting with 'p' vs others
# ============================================================================

cat("\n--- Q5 ---\n")
young <- young %>%
  mutate(starts_p = str_starts(Word, fixed("p")))

p_words     <- young %>% filter(starts_p)
other_words <- young %>% filter(!starts_p)

cat("Words starting with 'p': N =", nrow(p_words), "\n")
cat("Other words: N =", nrow(other_words), "\n")

ttest_result <- t.test(p_words$RT, other_words$RT, alternative="two.sided")
cat(sprintf("t = %.4f,  df = %.2f,  p = %.6f\n",
            ttest_result$statistic, ttest_result$parameter, ttest_result$p.value))
cat("Significant at 95%?", ifelse(ttest_result$p.value < 0.05, "YES", "NO"), "\n")
cat("Mean RT p-words:", mean(p_words$RT), "\n")
cat("Mean RT others: ", mean(other_words$RT), "\n")

# ============================================================================
# Q6 — Boxplot: noun RT vs verb RT  +  fivenum()
# ============================================================================

cat("\n--- Q6 ---\n")
noun_verb <- young %>% filter(WordCategory %in% c("N", "V"))

p6 <- ggplot(noun_verb, aes(x=WordCategory, y=RT, fill=WordCategory)) +
  geom_boxplot(alpha=0.75, outlier.colour="grey40", outlier.size=1) +
  scale_fill_manual(values=c("N"="#2196F3","V"="#F44336")) +
  labs(title="Reaction Times: Nouns vs Verbs (Young Subjects)",
       x="Word Category", y="RT") +
  theme_minimal(base_size=13) +
  theme(legend.position="none")

ggsave("results/Q6_boxplot_noun_verb.png", p6, width=7, height=6, dpi=150)

cat("fivenum — Nouns:\n"); print(fivenum(young$RT[young$WordCategory=="N"]))
cat("fivenum — Verbs:\n");  print(fivenum(young$RT[young$WordCategory=="V"]))

# ============================================================================
# Q7 — Bar plot with 95% CI: noun RT vs verb RT
# ============================================================================

cat("\n--- Q7 ---\n")
nv_summary <- noun_verb %>%
  group_by(WordCategory) %>%
  summarise(
    mean_RT = mean(RT),
    se_RT   = sd(RT) / sqrt(n()),
    ci95    = 1.96 * se_RT,
    .groups = "drop"
  )

p7 <- ggplot(nv_summary, aes(x=WordCategory, y=mean_RT, fill=WordCategory)) +
  geom_col(alpha=0.80) +
  geom_errorbar(aes(ymin=mean_RT - ci95, ymax=mean_RT + ci95),
                width=0.25, linewidth=0.9) +
  scale_fill_manual(values=c("N"="#2196F3","V"="#F44336")) +
  labs(title="Mean RT with 95% CI: Nouns vs Verbs (Young)",
       x="Word Category", y="Mean RT") +
  theme_minimal(base_size=13) +
  theme(legend.position="none")

ggsave("results/Q7_barplot_ci_noun_verb.png", p7, width=7, height=6, dpi=150)

# ============================================================================
# Q8 — Boxplot: mean RT by initial letter
# ============================================================================

cat("\n--- Q8 ---\n")
young <- young %>%
  mutate(first_letter = str_to_lower(str_sub(Word, 1, 1)))

p8 <- ggplot(young, aes(x=first_letter, y=RT)) +
  geom_boxplot(fill="#4CAF50", colour="grey30", alpha=0.70,
               outlier.size=0.7, outlier.colour="grey50") +
  labs(title="RT by Initial Letter of Word (Young Subjects)",
       x="Initial Letter", y="RT") +
  theme_minimal(base_size=12) +
  theme(axis.text.x = element_text(size=9))

ggsave("results/Q8_boxplot_by_letter.png", p8, width=14, height=6, dpi=150)

# ============================================================================
# Q9 — Words starting with two consonants vs all others
# ============================================================================

cat("\n--- Q9 ---\n")
vowels <- c("a","e","i","o","u")

starts_two_consonants <- function(word) {
  w <- str_to_lower(word)
  chars <- str_split(w, "")[[1]]
  length(chars) >= 2 &&
    !(chars[1] %in% vowels) &&
    !(chars[2] %in% vowels)
}

young <- young %>%
  rowwise() %>%
  mutate(two_cons = starts_two_consonants(Word)) %>%
  ungroup()

two_cons_words  <- young %>% filter(two_cons)
other_words2    <- young %>% filter(!two_cons)

cat("Two-consonant start words: N =", nrow(two_cons_words), "\n")
cat("Other words:               N =", nrow(other_words2), "\n")

# Welch t-test (unequal variances)
ttest_q9 <- t.test(two_cons_words$RT, other_words2$RT, alternative="two.sided")
cat(sprintf("Welch t = %.4f,  df = %.2f,  p = %.6f\n",
            ttest_q9$statistic, ttest_q9$parameter, ttest_q9$p.value))
cat("Significant at 95%?", ifelse(ttest_q9$p.value < 0.05, "YES", "NO"), "\n")
cat("Mean RT two-consonant words:", mean(two_cons_words$RT), "\n")
cat("Mean RT other words:        ", mean(other_words2$RT), "\n")

# Visualise
combined_q9 <- bind_rows(
  two_cons_words %>% mutate(Group="Two Consonants"),
  other_words2   %>% mutate(Group="Other")
)

p9 <- ggplot(combined_q9, aes(x=Group, y=RT, fill=Group)) +
  geom_boxplot(alpha=0.75) +
  scale_fill_manual(values=c("Two Consonants"="#FF9800","Other"="#607D8B")) +
  labs(title="RT: Words Starting with Two Consonants vs Others (Young)",
       x="Word Group", y="RT") +
  theme_minimal(base_size=13) +
  theme(legend.position="none")

ggsave("results/Q9_boxplot_two_consonants.png", p9, width=8, height=6, dpi=150)

# ============================================================================
# Done
# ============================================================================
cat("\n========================================\n")
cat("All analyses complete. Plots saved to results/\n")
cat("========================================\n")
