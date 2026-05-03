"""
Basic tests for ML Pipeline validation
"""
import pytest
import os
import yaml
import pandas as pd
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.train import load_config, preprocess_data


def test_config_exists():
    """Test that config file exists and can be loaded"""
    assert os.path.exists('config.yaml'), "config.yaml file not found"
    config = load_config()
    assert config is not None, "Config is None"
    assert 'data' in config, "Config missing 'data' section"
    assert 'model' in config, "Config missing 'model' section"
    assert 'mlflow' in config, "Config missing 'mlflow' section"


def test_config_structure():
    """Test that config has required fields"""
    config = load_config()
    
    # Test data section
    assert 'url' in config['data'], "Config data missing 'url'"
    assert 'test_size' in config['data'], "Config data missing 'test_size'"
    assert 'random_state' in config['data'], "Config data missing 'random_state'"
    
    # Test model section
    assert 'type' in config['model'], "Config model missing 'type'"
    assert 'params' in config['model'], "Config model missing 'params'"
    
    # Test mlflow section
    assert 'experiment_name' in config['mlflow'], "Config mlflow missing 'experiment_name'"
    assert 'tracking_uri' in config['mlflow'], "Config mlflow missing 'tracking_uri'"


def test_preprocessing_logic():
    """Test that preprocessing works with sample data"""
    config = load_config()
    
    # Create sample data similar to wine quality dataset
    sample_data = pd.DataFrame({
        'fixed acidity': [7.4, 7.8, 7.8],
        'volatile acidity': [0.7, 0.88, 0.76],
        'citric acid': [0.0, 0.0, 0.04],
        'residual sugar': [1.9, 2.6, 2.3],
        'chlorides': [0.076, 0.098, 0.092],
        'free sulfur dioxide': [11, 25, 15],
        'total sulfur dioxide': [34, 67, 54],
        'density': [0.9978, 0.9968, 0.997],
        'pH': [3.51, 3.2, 3.26],
        'sulphates': [0.56, 0.68, 0.65],
        'alcohol': [9.4, 9.8, 9.8],
        'quality': [5, 5, 7]
    })
    
    X, y = preprocess_data(sample_data, config)
    
    # Test outputs
    assert X is not None, "Features (X) is None"
    assert y is not None, "Target (y) is None"
    assert len(X) == len(y), "Features and target length mismatch"
    assert len(X) == 3, "Expected 3 samples"
    assert y.dtype == 'int64', "Target should be integer type"
    assert set(y.unique()).issubset({0, 1}), "Target should be binary (0 or 1)"


def test_data_directory_exists():
    """Test that data directory exists"""
    assert os.path.exists('data'), "data directory not found"


def test_src_directory_exists():
    """Test that src directory exists"""
    assert os.path.exists('src'), "src directory not found"
    assert os.path.exists('src/train.py'), "src/train.py not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
