import boto3
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
ENDPOINT_NAME = 'fraud-detection-endpoint'

# 1. Load one row of data to test with
df = pd.read_csv('data/raw/train.csv', header=None)
test_data = df.iloc[0, 1:] # Row 0, All columns except the target

# [THE FIX] Force comma-separated format manually
# We convert the numpy values to a simple list, then join them with commas
payload = ",".join(map(str, test_data.tolist()))

print(f"📤 Sending transaction data to AWS: \n{payload[:50]}...")

# 2. Invoke the Endpoint (The "Call")
runtime = boto3.client('sagemaker-runtime')

try:
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='text/csv',
        Body=payload
    )
    
    # 3. Read the Result
    result = response['Body'].read().decode('utf-8')
    
    # We strip any whitespace/newlines to be safe
    probability = float(result.strip())
    
    print("\n✅ API RESPONSE RECEIVED!")
    print(f"🔮 Fraud Probability: {probability:.4f}")
    
    if probability > 0.5:
        print("🚨 Verdict: FRAUD DETECTED")
    else:
        print("🟢 Verdict: LEGITIMATE TRANSACTION")

except Exception as e:
    print(f"\n❌ Error: {e}")