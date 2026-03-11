import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

def load_and_split_data(filepath, target_col='price', test_size=0.2):
    """Load data and split into train/test sets"""
    df = pd.read_csv(filepath)
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def train_models(X_train, y_train):
    """Train multiple regression models"""
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    trained_models = {}
    
    print("\n" + "=" * 50)
    print("TRAINING MODELS")
    print("=" * 50)
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model
        print(f"{name} trained successfully")
    
    return trained_models

def evaluate_models(models, X_test, y_test):
    """Evaluate all models and return metrics"""
    results = {}
    
    print("\n" + "=" * 50)
    print("MODEL EVALUATION")
    print("=" * 50)
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2
        }
        
        print(f"\n{name}:")
        print(f"  RMSE: ${rmse:,.2f}")
        print(f"  MAE:  ${mae:,.2f}")
        print(f"  R²:   {r2:.4f}")
    
    return results

def select_best_model(models, results):
    """Select the best model based on R² score"""
    best_model_name = max(results, key=lambda x: results[x]['R2'])
    best_model = models[best_model_name]
    
    print("\n" + "=" * 50)
    print(f"BEST MODEL: {best_model_name}")
    print(f"R² Score: {results[best_model_name]['R2']:.4f}")
    print("=" * 50)
    
    return best_model, best_model_name

def save_model(model, filepath='models/house_price_model.pkl'):
    """Save the trained model"""
    joblib.dump(model, filepath)
    print(f"\nModel saved to: {filepath}")

def train_pipeline(data_path='data/processed/engineered_data.csv'):
    """Main training pipeline"""
    print("=" * 50)
    print("HOUSE PRICE PREDICTION - MODEL TRAINING")
    print("=" * 50)
    
    # Load and split data
    X_train, X_test, y_train, y_test = load_and_split_data(data_path)
    
    # Train models
    models = train_models(X_train, y_train)
    
    # Evaluate models
    results = evaluate_models(models, X_test, y_test)
    
    # Select best model
    best_model, best_model_name = select_best_model(models, results)
    
    # Save best model
    save_model(best_model)
    
    # Save feature names
    feature_names = X_train.columns.tolist()
    joblib.dump(feature_names, 'models/feature_names.pkl')
    
    return best_model, results

if __name__ == "__main__":
    train_pipeline()
