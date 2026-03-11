from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model and preprocessing objects
MODEL_PATH = '../models/house_price_model.pkl'
SCALER_PATH = '../models/scaler.pkl'
FEATURE_NAMES_PATH = '../models/feature_names.pkl'

model = None
scaler = None
feature_names = None

def load_artifacts():
    """Load model and preprocessing artifacts"""
    global model, scaler, feature_names
    
    try:
        model = joblib.load(MODEL_PATH)
        print("✓ Model loaded successfully")
    except:
        print("✗ Model not found. Please train the model first.")
    
    try:
        scaler = joblib.load(SCALER_PATH)
        print("✓ Scaler loaded successfully")
    except:
        print("⚠ Scaler not found. Predictions without scaling.")
    
    try:
        feature_names = joblib.load(FEATURE_NAMES_PATH)
        print("✓ Feature names loaded successfully")
    except:
        print("⚠ Feature names not found.")

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
        
        # Convert to float
        features = {k: float(v) for k, v in data.items()}
        
        # Create DataFrame with correct feature order
        if feature_names:
            input_df = pd.DataFrame([features], columns=feature_names)
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
                             prediction=f"${prediction:,.2f}",
                             input_data=features)
    
    except Exception as e:
        return render_template('index.html', 
                             error=f"Error: {str(e)}")

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        # Create DataFrame
        if feature_names:
            input_df = pd.DataFrame([data], columns=feature_names)
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
            'formatted': f"${prediction:,.2f}"
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
    app.run(host='0.0.0.0', port=5000, debug=True)
