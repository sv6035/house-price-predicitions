import pandas as pd
import numpy as np

def generate_house_data(n_samples=1000):
    """Generate synthetic house price dataset"""
    np.random.seed(42)
    
    # Generate features
    area = np.random.normal(1800, 500, n_samples).clip(500, 5000)
    bedrooms = np.random.randint(1, 6, n_samples)
    bathrooms = np.random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4], n_samples)
    age = np.random.exponential(15, n_samples).clip(0, 100)
    location_score = np.random.uniform(1, 10, n_samples)
    
    # Generate price based on features with some noise
    base_price = 50000
    price = (
        base_price +
        area * 150 +
        bedrooms * 15000 +
        bathrooms * 20000 -
        age * 500 +
        location_score * 25000 +
        np.random.normal(0, 30000, n_samples)
    ).clip(50000, 2000000)
    
    # Create DataFrame
    df = pd.DataFrame({
        'area': area.round(2),
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age': age.round(1),
        'location_score': location_score.round(2),
        'price': price.round(2)
    })
    
    # Add some missing values (5%)
    for col in ['area', 'age', 'location_score']:
        mask = np.random.random(n_samples) < 0.05
        df.loc[mask, col] = np.nan
    
    return df

if __name__ == "__main__":
    print("Generating synthetic house price dataset...")
    
    df = generate_house_data(1000)
    
    # Save to CSV
    output_path = 'data/raw/house_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Dataset generated successfully!")
    print(f"✓ Saved to: {output_path}")
    print(f"\nDataset Info:")
    print(f"  Samples: {len(df)}")
    print(f"  Features: {df.shape[1] - 1}")
    print(f"\nColumn Descriptions:")
    print(f"  - area: House area in square feet (500-5000)")
    print(f"  - bedrooms: Number of bedrooms (1-5)")
    print(f"  - bathrooms: Number of bathrooms (1-4)")
    print(f"  - age: Age of house in years (0-100)")
    print(f"  - location_score: Location quality score (1-10)")
    print(f"  - price: House price in USD (target variable)")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nBasic Statistics:")
    print(df.describe())
