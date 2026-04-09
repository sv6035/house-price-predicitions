from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model and preprocessing objects
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'house_price_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
FEATURE_NAMES_PATH = os.path.join(BASE_DIR, 'models', 'feature_names.pkl')

model = None
scaler = None
feature_names = None

def load_artifacts():
    """Load model and preprocessing artifacts"""
    global model, scaler, feature_names
    
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
    except:
        print("Model not found. Please train the model first.")
    
    try:
        scaler = joblib.load(SCALER_PATH)
        print("Scaler loaded successfully")
    except:
        print("Scaler not found. Predictions without scaling.")
    
    try:
        feature_names = joblib.load(FEATURE_NAMES_PATH)
        print("Feature names loaded successfully")
    except:
        print("Feature names not found.")

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get input data from form
        data = request.form.to_dict()
        
        # Convert to float (except city)
        features = {}
        for k, v in data.items():
            if k == 'city':
                features[k] = v  # Keep as string
            else:
                features[k] = float(v)
        
        # Create engineered features
        features['total_rooms'] = features['bedrooms'] + features['bathrooms']
        # Don't create price_per_sqft as it's not available during prediction
        
        # Create age category (same logic as in feature engineering)
        age = features['age']
        if age <= 5:
            features['age_category'] = 0
        elif age <= 15:
            features['age_category'] = 1
        elif age <= 30:
            features['age_category'] = 2
        else:
            features['age_category'] = 3
        
        # Create city tier (Delhi = 2, Gurgaon = 1, Meerut = 0)
        city_map = {'Delhi': 2, 'Gurgaon': 1, 'Meerut': 0}
        features['city_tier'] = city_map.get(features.get('city'), 0)
        
        # Create DataFrame with correct feature order
        if feature_names:
            # Ensure we have all required features
            input_data = []
            for feature in feature_names:
                if feature == 'price_per_sqft':
                    continue  # Skip this feature as it's not available during prediction
                elif feature == 'city':
                    continue  # Skip original city column if it exists in feature names
                elif feature == 'is_premium_city':
                    input_data.append(features.get('city_tier', 0))  # Use city_tier for legacy feature
                else:
                    input_data.append(features[feature])
            
            # Filter feature names to exclude problematic features
            filtered_features = [f for f in feature_names if f not in ['city', 'price_per_sqft']]
            input_df = pd.DataFrame([input_data], columns=filtered_features)
        else:
            input_df = pd.DataFrame([features])
        
        # Scale features if scaler exists
        if scaler:
            input_scaled = scaler.transform(input_df)
        else:
            input_scaled = input_df.values
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        return render_template('index.html', 
                             prediction=f"Rs {prediction:,.0f}",
                             input_data=data)  # Use original form data
    
    except Exception as e:
        return render_template('index.html', 
                             error=f"Error: {str(e)}")

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        # Create engineered features
        data['total_rooms'] = data['bedrooms'] + data['bathrooms']
        data['price_per_sqft'] = 0  # Placeholder
        
        # Create age category
        age = data['age']
        if age <= 5:
            data['age_category'] = 0
        elif age <= 15:
            data['age_category'] = 1
        elif age <= 30:
            data['age_category'] = 2
        else:
            data['age_category'] = 3
        
        # Create DataFrame
        if feature_names:
            input_data = []
            for feature in feature_names:
                if feature == 'price_per_sqft':
                    input_data.append(0)
                else:
                    input_data.append(data[feature])
            input_df = pd.DataFrame([input_data], columns=feature_names)
        else:
            input_df = pd.DataFrame([data])
        
        # Scale and predict
        if scaler:
            input_scaled = scaler.transform(input_df)
        else:
            input_scaled = input_df.values
        
        prediction = model.predict(input_scaled)[0]
        
        return jsonify({
            'success': True,
            'prediction': float(prediction),
            'formatted': f"Rs {prediction:,.0f}"
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    load_artifacts()
    app.run(host='127.0.0.1', port=5000, debug=True)
