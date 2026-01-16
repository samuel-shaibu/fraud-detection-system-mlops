import boto3
import sagemaker
from sagemaker.inputs import TrainingInput

# --- CONFIGURATION ---
# Your specific bucket and role
BUCKET_NAME = "fraud-detection-197479160331" 
ROLE_ARN = "arn:aws:iam::197479160331:role/FraudSageMakerRole"

# 1. Setup Session
session = sagemaker.Session()
region = session.boto_region_name

# 2. Get the XGBoost Container Image (The "Chef")
container = sagemaker.image_uris.retrieve("xgboost", region, "latest")
print(f"🤖 Using Container: {container}")

# 3. Define the Training Job
xgb = sagemaker.estimator.Estimator(
    image_uri=container,
    role=ROLE_ARN,
    instance_count=1,
    instance_type='ml.m4.xlarge', # The Server Type (~$0.10/hour)
    output_path=f"s3://{BUCKET_NAME}/output",
    sagemaker_session=session
)

# 4. Set Hyperparameters
xgb.set_hyperparameters(
    objective='binary:logistic',
    num_round=50
)

# 5. Define Data Inputs
train_input = TrainingInput(
    f"s3://{BUCKET_NAME}/train/train.csv", content_type="csv"
)

# 6. START TRAINING
print("🚀 Starting Training Job... (This will take ~4 minutes)")
xgb.fit({'train': train_input})

print("✅ Training Finished!")