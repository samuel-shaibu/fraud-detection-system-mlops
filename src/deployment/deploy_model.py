import boto3
import sagemaker
import time
from sagemaker.model import Model
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
BUCKET_NAME = "fraud-detection-197479160331" 
ROLE_ARN = "arn:aws:iam::197479160331:role/FraudSageMakerRole"
ENDPOINT_NAME = 'fraud-detection-endpoint'

# The path where our Hybrid script saved the model
model_s3_path = f"s3://{BUCKET_NAME}/output/xgboost-model/model.tar.gz"

session = sagemaker.Session()
region = session.boto_region_name
sm_client = boto3.client('sagemaker', region_name=region)

print(f"🚀 Preparing to deploy model from: {model_s3_path}")

# --- 1. CLEANUP STEP ---
print("🧹 Checking for existing configurations...")

try:
    sm_client.delete_endpoint_config(EndpointConfigName=ENDPOINT_NAME)
    print(f"   - Deleted existing endpoint config: {ENDPOINT_NAME}")
    time.sleep(2)
except ClientError:
    pass 

try:
    sm_client.delete_endpoint(EndpointName=ENDPOINT_NAME)
    print(f"   - Deleted existing endpoint: {ENDPOINT_NAME}")
    time.sleep(5)
except ClientError:
    pass

# --- 2. DEPLOYMENT ---
print("📦 Loading model container...")

# [THE FIX] We explicitly ask for version 1.7-1 (Modern) instead of 'latest' (Old)
container = sagemaker.image_uris.retrieve("xgboost", region, "1.7-1")
print(f"   - Using container image: {container}")

model = Model(
    image_uri=container,
    model_data=model_s3_path,
    role=ROLE_ARN,
    sagemaker_session=session
)

print(f"⏳ Deploying to '{ENDPOINT_NAME}'... (This takes 5-8 minutes)")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium', 
    endpoint_name=ENDPOINT_NAME
)

print(f"✅ Success! Endpoint deployed at: {predictor.endpoint_name}")