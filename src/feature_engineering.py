import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

def create_features(df):
    """Create new features from existing ones"""
    print("\nCreating new features...")
    
    # Example: Total rooms
    if 'bedrooms' in df.columns and 'bathrooms' in df.columns:
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    
    # Example: Price per square foot (if price exists)
    if 'price' in df.columns and 'area' in df.columns:
        df['price_per_sqft'] = df['price'] / df['area']
    
    # Example: Age category - convert directly to numeric
    if 'age' in df.columns:
        df['age_category'] = pd.cut(df['age'], bins=[0, 5, 15, 30, 100], 
                                   labels=[0, 1, 2, 3])
    
    return df

def encode_categorical(df):
    """Encode all categorical variables"""
    print("\nEncoding categorical variables...")
    encoders = {}
    
    # Find all non-numeric columns
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            print(f"Encoded column: {col}")
    
    # Save encoders if any exist
    if encoders:
        joblib.dump(encoders, 'models/encoders.pkl')
    
    return df

def scale_features(df, feature_cols, target_col='price'):
    """Scale numerical features"""
    print("\nScaling features...")
    
    X = df[feature_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    df_scaled = pd.DataFrame(X_scaled, columns=feature_cols, index=df.index)
    
    if target_col in df.columns:
        df_scaled[target_col] = df[target_col].values
    
    # Save scaler
    joblib.dump(scaler, 'models/scaler.pkl')
    print(f"Scaled {len(feature_cols)} features")
    
    return df_scaled, scaler

def select_features(df, target_col='price', threshold=0.1):
    """Select features based on correlation with target"""
    print("\nSelecting features...")
    
    if target_col not in df.columns:
        return df.columns.tolist()
    
    correlations = df.corr()[target_col].abs().sort_values(ascending=False)
    selected = correlations[correlations > threshold].index.tolist()
    selected.remove(target_col)
    
    print(f"Selected {len(selected)} features with correlation > {threshold}")
    print(f"Features: {selected}")
    
    return selected

def engineer_features(input_path, output_path):
    """Main feature engineering pipeline"""
    print("=" * 50)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 50)
    
    df = pd.read_csv(input_path)
    print(f"Loaded data: {df.shape}")
    
    # Create new features
    df = create_features(df)
    
    # Encode all categorical variables
    df = encode_categorical(df)
    
    # Ensure all columns are numeric
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Scale features (excluding target column)
    target_col = 'price'
    feature_cols = [col for col in df.columns if col != target_col]
    
    if feature_cols:
        df_scaled, scaler = scale_features(df, feature_cols, target_col)
        df = df_scaled
        print(f"Features scaled and scaler saved")
    
    # Save processed data
    df.to_csv(output_path, index=False)
    print(f"\nEngineered data saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    engineer_features("data/processed/cleaned_data.csv", 
                      "data/processed/engineered_data.csv")
