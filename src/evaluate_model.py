import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

def load_model(model_path='models/house_price_model.pkl'):
    """Load the trained model"""
    return joblib.load(model_path)

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("=" * 50)
    print("MODEL EVALUATION METRICS")
    print("=" * 50)
    print(f"RMSE: ${rmse:,.2f}")
    print(f"MAE:  ${mae:,.2f}")
    print(f"R²:   {r2:.4f}")
    
    return y_pred, {'RMSE': rmse, 'MAE': mae, 'R2': r2}

def plot_predictions(y_test, y_pred, save_path='models/predictions_plot.png'):
    """Plot actual vs predicted values"""
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title('Actual vs Predicted House Prices')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"\nPrediction plot saved to: {save_path}")
    plt.close()

def plot_residuals(y_test, y_pred, save_path='models/residuals_plot.png'):
    """Plot residuals"""
    residuals = y_test - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Predicted Price')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Residual plot saved to: {save_path}")
    plt.close()

def feature_importance(model, feature_names, save_path='models/feature_importance.png'):
    """Plot feature importance (for tree-based models)"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]
        
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.title('Top 10 Feature Importances')
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Feature importance plot saved to: {save_path}")
        plt.close()

if __name__ == "__main__":
    # Load test data
    df = pd.read_csv('data/processed/engineered_data.csv')
    X = df.drop(columns=['price'])
    y = df['price']
    
    # Load model
    model = load_model()
    
    # Evaluate
    y_pred, metrics = evaluate_model(model, X, y)
    
    # Generate plots
    plot_predictions(y, y_pred)
    plot_residuals(y, y_pred)
    
    # Feature importance
    feature_names = joblib.load('models/feature_names.pkl')
    feature_importance(model, feature_names)
