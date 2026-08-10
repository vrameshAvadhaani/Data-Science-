import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

# Set random seed for reproducible portfolio dataset
np.random.seed(42)
random.seed(42)

# Configuration Constants
NUM_SESSIONS = 1000
START_DATE = datetime(2026, 7, 1, 8, 0, 0)

# KDP Beverages & Coffee Product Catalog Samples
BRANDS = ['Keurig', 'Dr Pepper', 'Snapple', "Peet's Coffee", "Mott's", 'Green Mountain', '7UP']
CATEGORIES = ['Coffee Pods', 'Carbonated Soft Drinks', 'Juice & Hydration', 'Coffee Makers']

SEARCH_QUERIES = [
    # High-intent Coffee Queries
    {'query': 'dark roast k-cup', 'category': 'Coffee Pods', 'expected_zero': False},
    {'query': 'vanilla flavored coffee', 'category': 'Coffee Pods', 'expected_zero': False},
    {'query': 'keurig single serve machine', 'category': 'Coffee Makers', 'expected_zero': False},
    {'query': 'espresso pods hazelnut', 'category': 'Coffee Pods', 'expected_zero': True}, # Niche zero-result query
    
    # High-intent Soda & Beverage Queries
    {'query': 'dr pepper zero sugar 12oz', 'category': 'Carbonated Soft Drinks', 'expected_zero': False},
    {'query': 'snapple peach tea diet', 'category': 'Juice & Hydration', 'expected_zero': False},
    {'query': 'cherry vanilla soda', 'category': 'Carbonated Soft Drinks', 'expected_zero': False},
    {'query': 'caffeine free organic energy drink', 'category': 'Juice & Hydration', 'expected_zero': True}, # Niche zero-result query
    
    # Generic / Misspelled Queries
    {'query': 'kcup pods discount', 'category': 'Coffee Pods', 'expected_zero': False},
    {'query': 'drpepr zero', 'category': 'Carbonated Soft Drinks', 'expected_zero': False}
]

# 1. Generate Dimension Table: Product Catalog
product_records = []
product_id_counter = 1001

for brand in BRANDS:
    for cat in CATEGORIES:
        for p in range(1, 4):
            product_records.append({
                'product_id': f"KDP_SKU_{product_id_counter}",
                'product_name': f"{brand} {cat} Pack {p*12}ct",
                'brand': brand,
                'category': cat,
                'unit_price': round(random.uniform(5.99, 49.99), 2)
            })
            product_id_counter += 1

df_catalog = pd.DataFrame(product_records)

# 2. Generate Fact Table: Raw Messy Clickstream Telemetry
events_list = []

for session_idx in range(NUM_SESSIONS):
    session_id = f"SES_{uuid.uuid4().hex[:10]}"
    user_id = f"USR_{random.randint(10000, 99999)}" if random.random() > 0.08 else None  # 8% missing user_id (Defect 1)
    
    # A/B Test Variant Assignment (50/50 Control vs Variant B)
    variant = 'Variant_B_AI_Semantic' if random.random() < 0.50 else 'Control_Keyword'
    device = random.choice(['desktop', 'mobile', 'tablet'])
    
    # Choose search query
    query_info = random.choice(SEARCH_QUERIES)
    query_text = query_info['query']
    
    # Experiment Effect: Variant B (AI Semantic) reduces zero-result searches and decreases latency
    if variant == 'Variant_B_AI_Semantic':
        results_count = 0 if (query_info['expected_zero'] and random.random() < 0.20) else random.randint(8, 45)
        latency_ms = random.randint(80, 220)
    else:
        results_count = 0 if (query_info['expected_zero'] and random.random() < 0.85) else random.randint(2, 25)
        latency_ms = random.randint(180, 650)
        
    zero_results_flag = (results_count == 0)
    session_start_time = START_DATE + timedelta(minutes=random.randint(0, 43200)) # Over 30 days
    
    # Event 1: search_query_submitted
    events_list.append({
        'event_id': f"EVT_{uuid.uuid4().hex[:8]}",
        'event_name': 'search_query_submitted',
        'timestamp': session_start_time,
        'session_id': session_id,
        'user_pseudo_id': user_id,
        'device_type': device,
        'experiment_variant': variant,
        'query_string': query_text,
        'results_count': results_count,
        'zero_results_flag': zero_results_flag,
        'latency_ms': latency_ms,
        'product_id': None,
        'rank_position': None,
        'cart_price': None
    })
    
    # --- DATA DEFECT 2: Double-click event duplication (10% chance) ---
    if random.random() < 0.10:
        events_list.append({
            'event_id': f"EVT_{uuid.uuid4().hex[:8]}",
            'event_name': 'search_query_submitted',
            'timestamp': session_start_time + timedelta(milliseconds=random.randint(100, 800)),
            'session_id': session_id,
            'user_pseudo_id': user_id,
            'device_type': device,
            'experiment_variant': variant,
            'query_string': query_text,
            'results_count': results_count,
            'zero_results_flag': zero_results_flag,
            'latency_ms': latency_ms,
            'product_id': None,
            'rank_position': None,
            'cart_price': None
        })

    # If search yielded results, simulate downstream interactions (Click & Cart Add)
    if not zero_results_flag:
        # Event 2: search_result_clicked
        if random.random() < (0.68 if variant == 'Variant_B_AI_Semantic' else 0.52):
            clicked_prod = df_catalog.sample(1).iloc[0]
            # Variant B ranks relevant items higher (Position #1-#3)
            rank_pos = random.randint(1, 3) if variant == 'Variant_B_AI_Semantic' else random.randint(1, 10)
            click_time = session_start_time + timedelta(seconds=random.randint(3, 15))
            
            events_list.append({
                'event_id': f"EVT_{uuid.uuid4().hex[:8]}",
                'event_name': 'search_result_clicked',
                'timestamp': click_time,
                'session_id': session_id,
                'user_pseudo_id': user_id,
                'device_type': device,
                'experiment_variant': variant,
                'query_string': query_text,
                'results_count': results_count,
                'zero_results_flag': False,
                'latency_ms': None,
                'product_id': clicked_prod['product_id'],
                'rank_position': rank_pos,
                'cart_price': None
            })
            
            # Event 3: search_to_cart_added
            if random.random() < (0.42 if variant == 'Variant_B_AI_Semantic' else 0.28):
                cart_time = click_time + timedelta(seconds=random.randint(5, 45))
                events_list.append({
                    'event_id': f"EVT_{uuid.uuid4().hex[:8]}",
                    'event_name': 'search_to_cart_added',
                    'timestamp': cart_time,
                    'session_id': session_id,
                    'user_pseudo_id': user_id,
                    'device_type': device,
                    'experiment_variant': variant,
                    'query_string': query_text,
                    'results_count': results_count,
                    'zero_results_flag': False,
                    'latency_ms': None,
                    'product_id': clicked_prod['product_id'],
                    'rank_position': rank_pos,
                    'cart_price': clicked_prod['unit_price']
                })

df_raw_telemetry = pd.DataFrame(events_list)

# --- DATA DEFECT 3: Out-of-order logging latency ---
df_raw_telemetry = df_raw_telemetry.sample(frac=1.0, random_state=42).reset_index(drop=True)

# Export Messy Native CSV Files
df_catalog.to_csv('dim_product_catalog.csv', index=False)
df_raw_telemetry.to_csv('raw_search_telemetry_logs.csv', index=False)

print(f"Native Data Generated Successfully!")
print(f"Catalog Products: {len(df_catalog)} SKUs")
print(f"Raw Telemetry Events: {len(df_raw_telemetry)} records (contains duplicates, missing IDs, out-of-order timestamps)")
