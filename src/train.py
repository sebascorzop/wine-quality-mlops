"""
Main training script for Wine Quality Prediction ML Pipeline
"""
import os
import yaml
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import requests
import json
from datetime import datetime

# Try to import MLflow, but make it optional
try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("Warning: MLflow not available. Metrics will be saved to file instead.")


def load_config(config_path="config.yaml"):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def download_data(url, output_path):
    """Download dataset from URL or generate synthetic data"""
    print(f"Attempting to download data from {url}...")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Data downloaded successfully to {output_path}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        print("Generating synthetic dataset instead...")
        
        # Import here to avoid circular dependency
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from generate_data import generate_wine_dataset
        
        df = generate_wine_dataset()
        df.to_csv(output_path, sep=';', index=False)
        
        print(f"Synthetic dataset generated and saved to {output_path}")
        return False


def load_data(config):
    """Load and prepare dataset"""
    data_path = config['data']['raw_path']
    
    # Download data if it doesn't exist
    if not os.path.exists(data_path):
        download_data(config['data']['url'], data_path)
    
    # Load data - try different separators
    try:
        df = pd.read_csv(data_path, sep=';')
    except:
        try:
            df = pd.read_csv(data_path, sep=',')
        except:
            df = pd.read_csv(data_path)
    
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return df


def preprocess_data(df, config):
    """Preprocess the dataset"""
    print("Preprocessing data...")
    
    # Handle missing values
    if config['preprocessing']['handle_missing'] == 'mean':
        df = df.fillna(df.mean())
    elif config['preprocessing']['handle_missing'] == 'drop':
        df = df.dropna()
    
    # Convert quality to binary classification (good: quality >= 6, bad: quality < 6)
    df['quality_class'] = (df['quality'] >= 6).astype(int)
    
    # Separate features and target
    X = df.drop(['quality', 'quality_class'], axis=1)
    y = df['quality_class']
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    return X, y


def split_data(X, y, config):
    """Split data into train and test sets"""
    test_size = config['data']['test_size']
    random_state = config['data']['random_state']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test, config):
    """Scale features if configured"""
    if config['preprocessing']['scale_features']:
        print("Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Convert back to DataFrame
        X_train = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    return X_train, X_test


def train_model(X_train, y_train, config):
    """Train the model"""
    print("Training model...")
    
    model_params = config['model']['params']
    model = RandomForestClassifier(**model_params)
    model.fit(X_train, y_train)
    
    print("Model training completed")
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the model"""
    print("Evaluating model...")
    
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred, average='weighted'),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted')
    }
    
    print("Evaluation metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  {metric_name}: {metric_value:.4f}")
    
    return metrics


def save_metrics_to_file(config, metrics, run_id=None):
    """Save metrics to JSON file when MLflow is not available"""
    os.makedirs('mlruns', exist_ok=True)
    
    results = {
        'run_id': run_id or datetime.now().strftime('%Y%m%d_%H%M%S'),
        'timestamp': datetime.now().isoformat(),
        'parameters': config['model']['params'],
        'metrics': metrics,
        'config': {
            'test_size': config['data']['test_size'],
            'scale_features': config['preprocessing']['scale_features']
        }
    }
    
    output_file = f"mlruns/results_{results['run_id']}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    return output_file


def main():
    """Main pipeline execution"""
    print("=" * 60)
    print("Wine Quality Prediction ML Pipeline")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    if MLFLOW_AVAILABLE:
        # Setup MLflow
        mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
        mlflow.set_experiment(config['mlflow']['experiment_name'])
        
        # Start MLflow run
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            
            # Load data
            df = load_data(config)
            
            # Preprocess data
            X, y = preprocess_data(df, config)
            
            # Split data
            X_train, X_test, y_train, y_test = split_data(X, y, config)
            
            # Scale features
            X_train, X_test = scale_features(X_train, X_test, config)
            
            # Train model
            model = train_model(X_train, y_train, config)
            
            # Evaluate model
            metrics = evaluate_model(model, X_test, y_test)
            
            # Log parameters to MLflow
            mlflow.log_params(config['model']['params'])
            mlflow.log_param("test_size", config['data']['test_size'])
            mlflow.log_param("scale_features", config['preprocessing']['scale_features'])
            
            # Log metrics to MLflow
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Create input example for model signature
            input_example = X_train.head(1)
            
            # Log model to MLflow
            mlflow.sklearn.log_model(
                model,
                "model",
                input_example=input_example,
                registered_model_name="wine_quality_classifier"
            )
            
            print("\n" + "=" * 60)
            print("Pipeline completed successfully with MLflow!")
            print(f"MLflow Run ID: {run_id}")
            print("=" * 60)
    else:
        # Run without MLflow
        print("\nRunning pipeline without MLflow tracking...")
        
        # Load data
        df = load_data(config)
        
        # Preprocess data
        X, y = preprocess_data(df, config)
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(X, y, config)
        
        # Scale features
        X_train, X_test = scale_features(X_train, X_test, config)
        
        # Train model
        model = train_model(X_train, y_train, config)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        
        # Save metrics to file
        results_file = save_metrics_to_file(config, metrics)
        
        # Save model using pickle
        import pickle
        model_path = 'mlruns/model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved to: {model_path}")
        
        print("\n" + "=" * 60)
        print("Pipeline completed successfully!")
        print(f"Results saved to: {results_file}")
        print("=" * 60)
        print("\nTo use MLflow tracking:")
        print("1. Install MLflow: pip install mlflow")
        print("2. Uncomment mlflow in requirements.txt")
        print("3. Run the pipeline again")


if __name__ == "__main__":
    main()
