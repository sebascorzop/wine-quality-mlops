"""
View results from ML pipeline runs
"""
import json
import os
from pathlib import Path

def view_results(mlruns_dir='mlruns'):
    """View all results from ML pipeline runs"""
    
    if not os.path.exists(mlruns_dir):
        print(f"No results directory found at {mlruns_dir}")
        return
    
    # Find all result JSON files
    result_files = list(Path(mlruns_dir).glob('results_*.json'))
    
    if not result_files:
        print("No result files found")
        return
    
    print("=" * 70)
    print("ML Pipeline Results Summary")
    print("=" * 70)
    print(f"\nTotal runs found: {len(result_files)}\n")
    
    for result_file in sorted(result_files, reverse=True):
        with open(result_file, 'r') as f:
            results = json.load(f)
        
        print("-" * 70)
        print(f"Run ID: {results['run_id']}")
        print(f"Timestamp: {results['timestamp']}")
        print("\nHyperparameters:")
        for param, value in results['parameters'].items():
            print(f"  {param}: {value}")
        
        print("\nConfiguration:")
        for key, value in results['config'].items():
            print(f"  {key}: {value}")
        
        print("\nPerformance Metrics:")
        for metric, value in results['metrics'].items():
            print(f"  {metric}: {value:.4f}")
        
        print()
    
    print("=" * 70)
    
    # Check for model file
    model_path = os.path.join(mlruns_dir, 'model.pkl')
    if os.path.exists(model_path):
        model_size = os.path.getsize(model_path) / 1024  # KB
        print(f"\n✓ Model saved: {model_path} ({model_size:.2f} KB)")
    else:
        print("\n✗ No model file found")
    
    print("=" * 70)

if __name__ == "__main__":
    view_results()
