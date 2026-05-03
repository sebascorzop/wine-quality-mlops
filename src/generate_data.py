"""
Generate synthetic wine quality dataset for testing
"""
import pandas as pd
import numpy as np

def generate_wine_dataset(n_samples=1599, random_state=42):
    """Generate synthetic wine quality dataset"""
    np.random.seed(random_state)
    
    # Generate features with realistic ranges
    data = {
        'fixed acidity': np.random.uniform(4.6, 15.9, n_samples),
        'volatile acidity': np.random.uniform(0.12, 1.58, n_samples),
        'citric acid': np.random.uniform(0.0, 1.0, n_samples),
        'residual sugar': np.random.uniform(0.9, 15.5, n_samples),
        'chlorides': np.random.uniform(0.012, 0.611, n_samples),
        'free sulfur dioxide': np.random.uniform(1.0, 72.0, n_samples),
        'total sulfur dioxide': np.random.uniform(6.0, 289.0, n_samples),
        'density': np.random.uniform(0.99007, 1.00369, n_samples),
        'pH': np.random.uniform(2.74, 4.01, n_samples),
        'sulphates': np.random.uniform(0.33, 2.0, n_samples),
        'alcohol': np.random.uniform(8.4, 14.9, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate quality based on some features with noise
    # Higher alcohol, lower volatile acidity -> better quality
    quality_score = (
        df['alcohol'] * 0.3 +
        (1 - df['volatile acidity']) * 20 +
        df['citric acid'] * 2 +
        np.random.normal(0, 1, n_samples)
    )
    
    # Convert to quality scale 3-8
    df['quality'] = np.clip(
        np.round((quality_score - quality_score.min()) / 
                 (quality_score.max() - quality_score.min()) * 5 + 3),
        3, 8
    ).astype(int)
    
    return df

if __name__ == "__main__":
    import os
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate dataset
    df = generate_wine_dataset()
    
    # Save with semicolon separator (like original UCI dataset)
    df.to_csv('data/winequality-red.csv', sep=';', index=False)
    
    print(f"Generated synthetic wine dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Quality distribution:\n{df['quality'].value_counts().sort_index()}")
    print(f"\nDataset saved to: data/winequality-red.csv")
