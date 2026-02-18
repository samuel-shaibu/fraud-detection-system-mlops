import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

# --- CONFIGURATION ---
EXPERIMENT_NAME = "Fraud_Detection_System"
DATA_PATH = 'data/raw/train.csv'

def train():
    print("🚀 Starting Training...")
    
    # 1. Setup MLflow
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    # 2. Load Data (THE FIX IS HERE)
    # We use header=None because the file has no column names.
    try:
        df = pd.read_csv(DATA_PATH, header=None)
    except FileNotFoundError:
        print(f"❌ Error: The file {DATA_PATH} was not found.")
        return

    # We assume Column 0 is the Target (0=Legit, 1=Fraud)
    # We rename it explicitly so we can drop it safely
    df.rename(columns={0: 'is_fraud'}, inplace=True)
    
    print(f"   - Loaded {len(df)} rows of data")
    print(f"   - Target distribution: \n{df['is_fraud'].value_counts()}")

    # 3. Split Features (X) and Target (y)
    X = df.drop('is_fraud', axis=1) # Drop the target column to get features
    y = df['is_fraud']              # This is our target
    
    # 4. Split into Train/Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Start MLflow Run
    with mlflow.start_run():
        print("🧠 Training XGBoost Model...")
        
        # Hyperparameters
        params = {
            "n_estimators": 100,
            "max_depth": 4,           # Increased slightly for better learning
            "learning_rate": 0.1,
            "objective": "binary:logistic",
            "eval_metric": "logloss"
        }
        
        # Log params to MLflow
        mlflow.log_params(params)
        
        # Train
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        # Predict
        predictions = model.predict(X_test)
        
        # Calculate Metrics
        acc = accuracy_score(y_test, predictions)
        # zero_division=0 prevents crashes if the model predicts only one class
        prec = precision_score(y_test, predictions, zero_division=0)
        rec = recall_score(y_test, predictions, zero_division=0)
        f1 = f1_score(y_test, predictions, zero_division=0)
        
        print(f"📊 Accuracy:  {acc:.4f}")
        print(f"📊 Precision: {prec:.4f}")
        print(f"📊 Recall:    {rec:.4f}")
        print(f"📊 F1 Score:  {f1:.4f}")
        
        # Log metrics to MLflow
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)
        
        # Log the actual model file so we can deploy it later
        mlflow.xgboost.log_model(model, "model")
        
        print("✅ Training Complete. Check MLflow dashboard!")

if __name__ == "__main__":
    train()