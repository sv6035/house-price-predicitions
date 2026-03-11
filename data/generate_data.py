import pandas as pd
import numpy as np

def generate_house_data(n_samples=1000):
    """Generate realistic house price dataset for Indian cities (Delhi, Meerut & Gurgaon)"""
    np.random.seed(42)
    
    # Define city data with realistic parameters
    cities = {
        'Delhi': {
            'base_price_per_sqft': 8000,  # Rs per sq ft
            'location_multiplier': (1.2, 2.5),  # Premium locations
            'samples': int(n_samples * 0.4)  # 40% Delhi
        },
        'Gurgaon': {
            'base_price_per_sqft': 6500,  # Rs per sq ft (Rapid Metro corridor)
            'location_multiplier': (1.0, 2.2),  # High-rise, metro connectivity
            'samples': int(n_samples * 0.35)  # 35% Gurgaon
        },
        'Meerut': {
            'base_price_per_sqft': 2500,  # Rs per sq ft  
            'location_multiplier': (0.8, 1.5),  # More affordable
            'samples': int(n_samples * 0.25)  # 25% Meerut
        }
    }
    
    all_data = []
    
    for city, params in cities.items():
        n_city = params['samples']
        base_price = params['base_price_per_sqft']
        loc_min, loc_max = params['location_multiplier']
        
        # Generate realistic features for Indian homes
        area = np.random.normal(1200, 400, n_city).clip(400, 3000)  # Sq ft
        bedrooms = np.random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5], n_city)  # More 2-3 BHK
        bathrooms = np.random.choice([1, 1.5, 2, 2, 2.5, 3, 3.5, 4], n_city)
        
        # Age distribution (Indian real estate)
        age = np.random.choice(
            [0, 1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40], 
            n_city, 
            p=[0.05, 0.08, 0.12, 0.15, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04, 0.03, 0.02]
        )
        
        # Location scores (1-10, where 10 is premium)
        if city == 'Delhi':
            # Delhi has more premium locations
            location_score = np.random.beta(2, 3, n_city) * 9 + 1  # Skewed towards higher
        elif city == 'Gurgaon':
            # Gurgaon has modern developments, metro connectivity
            location_score = np.random.beta(2.5, 2.5, n_city) * 8.5 + 1.5  # High average
        else:
            # Meerut has more mid-range locations
            location_score = np.random.beta(3, 2, n_city) * 8 + 1  # More normal distribution
        
        # Calculate realistic prices
        price_per_sqft = base_price * np.random.uniform(loc_min, loc_max, n_city)
        
        # Price adjustments based on features
        bedroom_bonus = (bedrooms - 2) * 200  # Rs per sq ft bonus for more bedrooms
        bathroom_bonus = (bathrooms - 1) * 150  # Rs per sq ft bonus for more bathrooms
        age_penalty = age * 50  # Rs per sq ft penalty for older homes
        location_bonus = (location_score - 5) * 300  # Location premium
        
        adjusted_price_per_sqft = (
            price_per_sqft + 
            bedroom_bonus + 
            bathroom_bonus - 
            age_penalty + 
            location_bonus
        ).clip(1000, 25000)  # Reasonable bounds
        
        # Total price
        total_price = (area * adjusted_price_per_sqft).clip(500000, 50000000)  # 5L to 5Cr
        
        # Add some market noise
        market_noise = np.random.normal(1, 0.15, n_city)  # ±15% variation
        total_price = total_price * market_noise
        
        # Create city data
        city_data = pd.DataFrame({
            'area': area.round(0).astype(int),
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'age': age,
            'location_score': location_score.round(1),
            'city': city,
            'price': total_price.round(0).astype(int)
        })
        
        all_data.append(city_data)
    
    # Combine all cities
    df = pd.concat(all_data, ignore_index=True)
    
    # Add some missing values (realistic 3%)
    missing_cols = ['area', 'age', 'location_score']
    for col in missing_cols:
        mask = np.random.random(len(df)) < 0.03
        df.loc[mask, col] = np.nan
    
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    print("Generating realistic Indian house price dataset...")
    print("Cities: Delhi (Premium) • Gurgaon (Rapid Metro) • Meerut (Affordable)")
    
    df = generate_house_data(1000)
    
    # Save to CSV
    output_path = 'data/raw/house_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"Saved to: {output_path}")
    print(f"\nDataset Info:")
    print(f"  Total Samples: {len(df)}")
    print(f"  Features: {df.shape[1] - 1}")
    
    # City breakdown
    city_counts = df['city'].value_counts()
    print(f"\nCity Distribution:")
    for city, count in city_counts.items():
        avg_price = df[df['city'] == city]['price'].mean()
        print(f"  {city}: {count} properties (Avg: Rs {avg_price:,.0f})")
    
    print(f"\nColumn Descriptions:")
    print(f"  - area: House area in square feet (400-3000)")
    print(f"  - bedrooms: Number of bedrooms (1-5, mostly 2-3 BHK)")
    print(f"  - bathrooms: Number of bathrooms (1-4)")
    print(f"  - age: Age of property in years (0-40)")
    print(f"  - location_score: Location quality score (1-10)")
    print(f"  - city: Delhi (premium) or Meerut (affordable)")
    print(f"  - price: Property price in Indian Rupees")
    
    print(f"\nPrice Statistics:")
    print(f"  Min Price: Rs {df['price'].min():,}")
    print(f"  Max Price: Rs {df['price'].max():,}")
    print(f"  Avg Price: Rs {df['price'].mean():,.0f}")
    print(f"  Median Price: Rs {df['price'].median():,.0f}")
    
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    print(f"\nSample by City:")
    for city in df['city'].unique():
        print(f"\n{city} Sample:")
        city_sample = df[df['city'] == city].head(3)
        for _, row in city_sample.iterrows():
            print(f"  {row['bedrooms']}BHK, {row['area']}sqft, {row['age']}yrs old -> Rs {row['price']:,}")
