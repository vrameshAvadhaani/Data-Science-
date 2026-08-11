import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest

# 1. Load the cleaned fact dataset from Day 1
df_telemetry = pd.read_csv('02_data_pipeline/fact_search_telemetry_clean.csv')

print("=" * 65)
print("     DIGITAL SHELF SEARCH A/B EXPERIMENT EVALUATION ENGINE     ")
print("=" * 65)

# Extract Search Submissions (Total Users/Sessions in Experiment)
df_searches = df_telemetry[df_telemetry['event_name'] == 'search_query_submitted'].copy()

# Extract Add-to-Cart Conversions
df_conversions = df_telemetry[df_telemetry['event_name'] == 'search_to_cart_added'].copy()

# Aggregate totals by variant
control_sessions = df_searches[df_searches['experiment_variant'] == 'Control_Keyword']['session_id'].nunique()
variant_sessions = df_searches[df_searches['experiment_variant'] == 'Variant_B_AI_Semantic']['session_id'].nunique()

control_conversions = df_conversions[df_conversions['experiment_variant'] == 'Control_Keyword']['session_id'].nunique()
variant_conversions = df_conversions[df_conversions['experiment_variant'] == 'Variant_B_AI_Semantic']['session_id'].nunique()

total_sessions = control_sessions + variant_sessions

print(f"\n[EXPERIMENT SAMPLE SIZES]")
print(f"Total Search Sessions: {total_sessions:,}")
print(f" - Control (Keyword Search)    : {control_sessions:,} sessions")
print(f" - Variant B (AI Semantic)     : {variant_sessions:,} sessions")

# --------------------------------------------------------------------
# STEP 1: SAMPLE RATIO MISMATCH (SRM) CHI-SQUARE TEST
# --------------------------------------------------------------------
print("\n" + "-" * 65)
print("STEP 1: SAMPLE RATIO MISMATCH (SRM) INTEGRITY CHECK")
print("-" * 65)

expected_traffic = [total_sessions * 0.50, total_sessions * 0.50]
observed_traffic = [control_sessions, variant_sessions]

chi2_stat, srm_p_value = stats.chisquare(f_obs=observed_traffic, f_exp=expected_traffic)

print(f"Expected Split : 50% / 50% ({int(expected_traffic[0])} vs {int(expected_traffic[1])})")
print(f"Observed Split : {control_sessions / total_sessions:.1%} / {variant_sessions / total_sessions:.1%}")
print(f"Chi-Square Stat: {chi2_stat:.4f} | SRM p-value: {srm_p_value:.4f}")

if srm_p_value < 0.01:
    print("❌ SRM ALERT: Sample Ratio Mismatch detected! Traffic assignment bug present. INVALIDATE TEST.")
else:
    print("✅ SRM PASSED: Traffic assignment is unbiased (50/50 split validated). Proceeding to hypothesis testing.")

# --------------------------------------------------------------------
# STEP 2: TWO-SAMPLE Z-TEST FOR CONVERSION UPLIFT
# --------------------------------------------------------------------
print("\n" + "-" * 65)
print("STEP 2: PRIMARY HYPOTHESIS TESTING (SEARCH-TO-CART CONVERSION)")
print("-" * 65)

cr_control = control_conversions / control_sessions
cr_variant = variant_conversions / variant_sessions
absolute_lift = cr_variant - cr_control
relative_lift = (cr_variant - cr_control) / cr_control

# Run Z-test for proportions
counts = np.array([variant_conversions, control_conversions])
nobs = np.array([variant_sessions, control_sessions])
z_stat, p_value = proportions_ztest(counts, nobs, alternative='two-sided')

# Compute 95% Confidence Interval for Difference
se_diff = np.sqrt((cr_control * (1 - cr_control) / control_sessions) + (cr_variant * (1 - cr_variant) / variant_sessions))
ci_lower = absolute_lift - (1.96 * se_diff)
ci_upper = absolute_lift + (1.96 * se_diff)

print(f"Control Conversion Rate   : {cr_control:.2%}")
print(f"Variant B Conversion Rate : {cr_variant:.2%}")
print(f"Absolute Conversion Lift  : {absolute_lift:+.2%} points")
print(f"Relative Conversion Lift  : {relative_lift:+.2%}")
print(f"Z-Score Statistic         : {z_stat:.4f}")
print(f"p-Value                   : {p_value:.5f}")
print(f"95% Confidence Interval   : [{ci_lower:+.2%}, {ci_upper:+.2%}]")

if p_value < 0.05:
    print("\n🎉 RESULT: STATISTICALLY SIGNIFICANT WIN! (p < 0.05)")
    print("Variant B (AI Semantic Search) demonstrates a statistically significant uplift in conversion rate.")
else:
    print("\n⚠️ RESULT: INCONCLUSIVE / NEUTRAL (p >= 0.05)")
    print("Failed to reject the Null Hypothesis. Insufficient evidence that Variant B improves conversion.")

# --------------------------------------------------------------------
# STEP 3: GUARDRAIL METRIC EVALUATION (SITE SPEED LATENCY)
# --------------------------------------------------------------------
print("\n" + "-" * 65)
print("STEP 3: GUARDRAIL METRIC EVALUATION (P95 LATENCY IMPACT)")
print("-" * 65)

latency_control_p95 = df_searches[df_searches['experiment_variant'] == 'Control_Keyword']['latency_ms'].quantile(0.95)
latency_variant_p95 = df_searches[df_searches['experiment_variant'] == 'Variant_B_AI_Semantic']['latency_ms'].quantile(0.95)

print(f"Control P95 Latency   : {latency_control_p95:.1f} ms")
print(f"Variant B P95 Latency : {latency_variant_p95:.1f} ms")
print(f"Latency Impact        : {latency_variant_p95 - latency_control_p95:+.1f} ms")

if latency_variant_p95 < 500:
    print("✅ GUARDRAIL PASSED: P95 Latency remains well within acceptable SLA threshold (<500ms).")
else:
    print("⚠️ GUARDRAIL WARNING: Variant B exceeds latency SLAs. Require engineering optimization before 100% rollout.")

print("\n" + "=" * 65)
