import pandas as pd
import numpy as np

def load_data(filepath):
    """Load dataset from CSV file"""
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print(f"\nMissing values before cleaning:\n{df.isnull().sum()}")
    
    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    print(f"\nMissing values after cleaning:\n{df.isnull().sum()}")
    return df

def remove_duplicates(df):
    """Remove duplicate rows"""
    initial_rows = df.shape[0]
    df = df.drop_duplicates()
    removed = initial_rows - df.shape[0]
    print(f"\nRemoved {removed} duplicate rows")
    return df

def remove_outliers(df, columns, threshold=3):
    """Remove outliers using Z-score method"""
    initial_rows = df.shape[0]
    for col in columns:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        df = df[z_scores < threshold]
    removed = initial_rows - df.shape[0]
    print(f"\nRemoved {removed} outlier rows")
    return df

def clean_data(input_path, output_path):
    """Main data cleaning pipeline"""
    print("=" * 50)
    print("DATA CLEANING PIPELINE")
    print("=" * 50)
    
    df = load_data(input_path)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    print(f"Final dataset shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    clean_data("data/raw/house_data.csv", "data/processed/cleaned_data.csv")
