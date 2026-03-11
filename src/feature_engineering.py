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
    
    # Example: Age category
    if 'age' in df.columns:
        df['age_category'] = pd.cut(df['age'], bins=[0, 5, 15, 30, 100], 
                                     labels=['new', 'recent', 'old', 'very_old'])
    
    return df

def encode_categorical(df, categorical_cols):
    """Encode categorical variables"""
    print("\nEncoding categorical variables...")
    encoders = {}
    
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    
    # Save encoders
    joblib.dump(encoders, 'models/encoders.pkl')
    print(f"Encoded columns: {categorical_cols}")
    
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
    
    # Identify categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        df = encode_categorical(df, categorical_cols)
    
    # Save processed data
    df.to_csv(output_path, index=False)
    print(f"\nEngineered data saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    engineer_features("data/processed/cleaned_data.csv", 
                      "data/processed/engineered_data.csv")
