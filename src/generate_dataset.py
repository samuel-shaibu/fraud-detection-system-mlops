import pandas as pd
import random
import os  # <--- Added this
from faker import Faker

fake = Faker()
NUM_ROWS = 2000

print(f"🔄 Generating {NUM_ROWS} transactions...")

data = []
for _ in range(NUM_ROWS):
    is_fraud = 0
    amount = round(random.uniform(10, 500), 2)
    
    if random.random() > 0.95:
        amount = round(random.uniform(800, 5000), 2)
        is_fraud = 1
        
    transaction = {
        'is_fraud': is_fraud,
        'amount': amount,
        'distance_from_home': round(random.uniform(1, 100), 2),
        'hour_of_day': random.randint(0, 23)
    }
    data.append(transaction)

df = pd.DataFrame(data)

# --- THE FIX STARTS HERE ---
# 1. Build a safe path for Windows/Linux
output_dir = os.path.join('data', 'raw')
output_file = os.path.join(output_dir, 'train.csv')

# 2. Force create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# 3. Save
df.to_csv(output_file, index=False, header=False)
# --- THE FIX ENDS HERE ---

print(f"✅ Saved {output_file} with {len(df)} rows.")
print(df.head())