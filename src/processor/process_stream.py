import base64
import json
import boto3
import os

# CONFIGURATION
ENDPOINT_NAME = 'fraud-detection-endpoint'
runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    print(f"🔄 Processing {len(event['Records'])} records...")
    
    for record in event['Records']:
        try:
            # 1. Decode the Kinesis Data
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            transaction = json.loads(payload)
            
            # 2. SMART FILTER: Keep ONLY numbers (Integers and Floats)
            # This automatically strips out Names, Cities, Dates, etc.
            features = [value for value in transaction.values() if isinstance(value, (int, float))]
            
            # Convert to CSV format (String)
            csv_data = ",".join(map(str, features))
            
            print(f"📤 Sending numeric data to Model: {csv_data[:50]}...")
            
            # 3. Call SageMaker
            response = runtime.invoke_endpoint(
                EndpointName=ENDPOINT_NAME,
                ContentType='text/csv',
                Body=csv_data
            )
            
            result = response['Body'].read().decode('utf-8')
            probability = float(result.strip())
            
            # 4. Determine Verdict
            verdict = "🚨 FRAUD" if probability > 0.5 else "✅ LEGIT"
            
            # We try to grab a name for the log, or default to "Unknown"
            # Assuming 'name' might be a key in the transaction, or we grab the 2nd value
            values_list = list(transaction.values())
            customer_name = values_list[1] if len(values_list) > 1 else "Customer"
            
            print(f"🔮 {verdict} | {customer_name} | Prob: {probability:.4f}")
            
        except Exception as e:
            # We print the error but don't crash the loop
            print(f"❌ Error: {str(e)}")
            
    return {"statusCode": 200, "body": "Processed"}