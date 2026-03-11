#!/usr/bin/env python3
"""
Test script to verify the Flask app works correctly
"""

import sys
import os
sys.path.append('app')

# Change to app directory for correct relative paths
os.chdir('app')

import app

def test_app():
    """Test the Flask app functionality"""
    print("=" * 50)
    print("TESTING FLASK APP")
    print("=" * 50)
    
    # Load artifacts
    print("\n1. Loading model artifacts...")
    app.load_artifacts()
    
    if not app.model:
        print("ERROR: Model not loaded!")
        return False
    
    if not app.scaler:
        print("ERROR: Scaler not loaded!")
        return False
    
    if not app.feature_names:
        print("ERROR: Feature names not loaded!")
        return False
    
    print(f"   Expected features: {app.feature_names}")
    
    # Test prediction
    print("\n2. Testing prediction...")
    test_data = {
        'area': 1800,
        'bedrooms': 3,
        'bathrooms': 2,
        'age': 10,
        'location_score': 7.5
    }
    
    try:
        # Create engineered features (same logic as in app)
        features = test_data.copy()
        features['total_rooms'] = features['bedrooms'] + features['bathrooms']
        features['price_per_sqft'] = 0
        
        # Age category
        age = features['age']
        if age <= 5:
            features['age_category'] = 0
        elif age <= 15:
            features['age_category'] = 1
        elif age <= 30:
            features['age_category'] = 2
        else:
            features['age_category'] = 3
        
        # Create input array in correct order
        input_data = [features[feature] for feature in app.feature_names]
        
        # Scale and predict
        import pandas as pd
        df = pd.DataFrame([input_data], columns=app.feature_names)
        scaled = app.scaler.transform(df)
        prediction = app.model.predict(scaled)[0]
        
        print(f"   Input: {test_data}")
        print(f"   Prediction: ${prediction:,.2f}")
        
        if prediction > 0:
            print("   SUCCESS: Prediction successful!")
        else:
            print("   ERROR: Invalid prediction!")
            return False
            
    except Exception as e:
        print(f"   ERROR: Prediction failed: {e}")
        return False
    
    print("\n3. App ready for deployment!")
    print("\nTo start the app:")
    print("   cd app")
    print("   python app.py")
    print("   Open browser: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = test_app()
    if success:
        print("\n" + "=" * 50)
        print("SUCCESS: ALL TESTS PASSED - APP IS READY!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("ERROR: TESTS FAILED - CHECK ERRORS ABOVE")
        print("=" * 50)
        sys.exit(1)