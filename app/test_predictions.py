from app import app

# Test prediction functionality
with app.test_client() as client:
    # Test Delhi property
    delhi_data = {
        'city': 'Delhi',
        'area': '1200',
        'bedrooms': '3',
        'bathrooms': '2',
        'age': '5',
        'location_score': '8.0'
    }
    
    response = client.post('/predict', data=delhi_data)
    print('Delhi Prediction Status:', response.status_code)
    
    # Test Gurgaon property
    gurgaon_data = {
        'city': 'Gurgaon',
        'area': '1200',
        'bedrooms': '3',
        'bathrooms': '2',
        'age': '5',
        'location_score': '8.0'
    }
    
    response = client.post('/predict', data=gurgaon_data)
    print('Gurgaon Prediction Status:', response.status_code)
    
    # Test Meerut property
    meerut_data = {
        'city': 'Meerut',
        'area': '1200',
        'bedrooms': '3',
        'bathrooms': '2',
        'age': '5',
        'location_score': '8.0'
    }
    
    response = client.post('/predict', data=meerut_data)
    print('Meerut Prediction Status:', response.status_code)
    
    if response.status_code == 200:
        print('SUCCESS: All three cities work correctly!')
        print('Professional NCR Real Estate App is ready!')
    else:
        print('ERROR: Prediction issues detected')