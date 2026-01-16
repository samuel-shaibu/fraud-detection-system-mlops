import boto3
import json
import time
import random
from faker import Faker

# 1. Setup the "Fake Data" generator
fake = Faker()

# 2. Setup the connection to AWS Kinesis
# We use us-east-1 because that is what you configured in the CLI
kinesis_client = boto3.client('kinesis', region_name='us-east-1') 
STREAM_NAME = 'fraud-detection-stream'

def generate_transaction():
    """Creates a fake dictionary representing a swipe"""
    transaction = {
        'transaction_id': fake.uuid4(),
        'name': fake.name(),
        'amount': round(random.uniform(10, 1000), 2), # Random amount $10-$1000
        'timestamp': time.time(),
        'location': fake.city()
    }
    return transaction

print(f"🌊 Sending data to stream: {STREAM_NAME}...")

while True:
    # 3. Generate 1 transaction
    data = generate_transaction()
    
    # 4. Convert dict to JSON (Text)
    data_json = json.dumps(data)
    
    # 5. Send it to Kinesis!
    try:
        kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=data_json,
            PartitionKey=data['transaction_id']
        )
        print(f"Sent: {data}")
    except Exception as e:
        print(f"❌ Error sending data: {e}")
    
    # 6. Wait a bit so we don't spam too fast
    time.sleep(1)