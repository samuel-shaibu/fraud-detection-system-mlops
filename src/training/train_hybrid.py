import boto3
import xgboost as xgb
import pandas as pd
import tarfile
import os

# --- CONFIGURATION ---
BUCKET_NAME = "fraud-detection-197479160331" 
LOCAL_MODEL_NAME = "xgboost-model"

print("🚀 Starting Hybrid Training (Local CPU)...")

# 1. Load Data (We use the local file we generated earlier)
df = pd.read_csv('data/raw/train.csv', header=None)
X = df.iloc[:, 1:] # Features
y = df.iloc[:, 0]  # Target

# 2. Train the Model Locally
# We use the same algorithm SageMaker would use
model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='error')
model.fit(X, y)
print("✅ Model Trained successfully on laptop.")

# 3. Save model in the format SageMaker expects
# SageMaker requires the file to be named specific things based on version
model.save_model(LOCAL_MODEL_NAME)

# 4. Zip it into model.tar.gz (Required by SageMaker)
with tarfile.open("model.tar.gz", "w:gz") as tar:
    tar.add(LOCAL_MODEL_NAME)
    
print("📦 Model packaged into model.tar.gz")

# 5. Upload to S3 (So SageMaker Deployment can find it)
s3 = boto3.client('s3')
s3_path = f"output/{LOCAL_MODEL_NAME}/model.tar.gz"

print(f"☁️ Uploading to s3://{BUCKET_NAME}/{s3_path}...")
s3.upload_file("model.tar.gz", BUCKET_NAME, s3_path)

# Cleanup local files
os.remove(LOCAL_MODEL_NAME)
os.remove("model.tar.gz")

print(f"🎉 Success! Your model is now in the cloud, ready for SageMaker Deployment.")