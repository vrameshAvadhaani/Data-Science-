import pandas as pd

# Load native messy files
df_raw = pd.read_csv('raw_search_telemetry_logs.csv')

print(f"Initial Raw Record Count: {len(df_raw)}")

# 1. Parse Datetime fields
df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'])

# 2. Impute or flag missing User Pseudo IDs
df_raw['user_pseudo_id'] = df_raw['user_pseudo_id'].fillna('ANONYMOUS_GUEST')

# 3. Deduplicate Double-Click Triggers
# Sort by session, event_name, query_string, and timestamp
df_raw = df_raw.sort_values(by=['session_id', 'event_name', 'query_string', 'timestamp'])

# Calculate time difference between consecutive identical events in the same session
df_raw['prev_timestamp'] = df_raw.groupby(['session_id', 'event_name', 'query_string'])['timestamp'].shift(1)
df_raw['time_diff_sec'] = (df_raw['timestamp'] - df_raw['prev_timestamp']).dt.total_seconds()

# Filter out duplicate events logged within 2 seconds of each other
df_clean = df_raw[(df_raw['time_diff_sec'].isna()) | (df_raw['time_diff_sec'] > 2.0)].copy()

# Drop temporary calculation columns
df_clean = df_clean.drop(columns=['prev_timestamp', 'time_diff_sec'])

# 4. Re-order Chronologically (Fixing out-of-order latency issue)
df_clean = df_clean.sort_values(by='timestamp').reset_index(drop=True)

print(f"Cleaned Record Count: {len(df_clean)} (Removed {len(df_raw) - len(df_clean)} duplicate/noisy events)")

# Save Refined Fact Table
df_clean.to_csv('fact_search_telemetry_clean.csv', index=False)
print("Saved cleaned dataset to 'fact_search_telemetry_clean.csv'")
