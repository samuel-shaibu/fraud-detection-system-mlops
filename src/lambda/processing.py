import json
import base64

def lambda_handler(event, context):
    """
    This function triggers whenever Kinesis has new data.
    'event' contains a batch of records.
    """
    print(f"⚡ Event received! Found {len(event['Records'])} records.")

    for record in event['Records']:
        # 1. Kinesis data is Base64 encoded. We must decode it.
        # Kinesis stores data as bytes, so we decode to string.
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        
        # 2. Convert string back to JSON dictionary
        transaction = json.loads(payload)
        
        # 3. Simple Rule (Feature Engineering Logic)
        amount = transaction['amount']
        status = "✅ LEGIT"
        if amount > 900:
            status = "🚨 HIGH VALUE - CHECK"
            
        print(f"Processing ID: {transaction['transaction_id']} | Amount: ${amount} | Status: {status}")

    return {
        'statusCode': 200,
        'body': json.dumps('Batch Processed Successfully')
    }