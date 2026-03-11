"""
Main pipeline script to run the complete house price prediction workflow
"""
import sys
import os

# Add src to path
sys.path.append('src')

from data_cleaning import clean_data
from feature_engineering import engineer_features
from train_model import train_pipeline

def run_pipeline():
    """Execute the complete ML pipeline"""
    print("\n" + "=" * 60)
    print("HOUSE PRICE PREDICTION - COMPLETE PIPELINE")
    print("=" * 60)
    
    # Step 1: Data Cleaning
    print("\n[STEP 1/3] Data Cleaning...")
    clean_data('data/raw/house_data.csv', 'data/processed/cleaned_data.csv')
    
    # Step 2: Feature Engineering
    print("\n[STEP 2/3] Feature Engineering...")
    engineer_features('data/processed/cleaned_data.csv', 
                     'data/processed/engineered_data.csv')
    
    # Step 3: Model Training
    print("\n[STEP 3/3] Model Training...")
    model, results = train_pipeline('data/processed/engineered_data.csv')
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review model performance in the results above")
    print("2. Run 'python src/evaluate_model.py' for detailed evaluation")
    print("3. Start the Flask app: 'cd app && python app.py'")
    print("4. Open browser at http://localhost:5000")
    
    return model, results

if __name__ == "__main__":
    run_pipeline()
