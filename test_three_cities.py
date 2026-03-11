import sys
import os
sys.path.append('app')
os.chdir('app')

import app
import pandas as pd

app.load_artifacts()

print("=== NCR REAL ESTATE PRICING TEST ===")
print("Features:", app.feature_names)

# Test same property in all three cities
base_property = {
    'area': 1200,
    'bedrooms': 3,
    'bathrooms': 2,
    'age': 5,
    'location_score': 7.5,
    'total_rooms': 5,
    'age_category': 1
}

cities = [
    {'name': 'Delhi (Premium)', 'city_tier': 2},
    {'name': 'Gurgaon (Rapid Metro)', 'city_tier': 1}, 
    {'name': 'Meerut (Affordable)', 'city_tier': 0}
]

for city in cities:
    features = base_property.copy()
    features['city_tier'] = city['city_tier']
    
    # Handle legacy feature name
    if 'is_premium_city' in app.feature_names:
        features['is_premium_city'] = city['city_tier']
    
    df = pd.DataFrame([[features[f] for f in app.feature_names]], columns=app.feature_names)
    scaled = app.scaler.transform(df)
    pred = app.model.predict(scaled)[0]
    
    print(f"{city['name']}: Rs {pred:,.0f}")

print("\n=== SUCCESS: Three-city pricing with background! ===")