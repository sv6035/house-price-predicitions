"""
Test script to verify the house price prediction system setup
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    
    packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'flask',
        'joblib'
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT FOUND")
            failed.append(package)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True

def test_directory_structure():
    """Test if all required directories exist"""
    print("\nTesting directory structure...")
    
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'notebooks',
        'src',
        'models',
        'app',
        'app/templates'
    ]
    
    failed = []
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ - NOT FOUND")
            failed.append(directory)
    
    if failed:
        print(f"\n❌ Missing directories: {', '.join(failed)}")
        return False
    else:
        print("\n✅ All directories exist!")
        return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting required files...")
    
    files = [
        'requirements.txt',
        'README.md',
        'run_pipeline.py',
        'data/generate_data.py',
        'src/data_cleaning.py',
        'src/feature_engineering.py',
        'src/train_model.py',
        'src/evaluate_model.py',
        'app/app.py',
        'app/templates/index.html'
    ]
    
    failed = []
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            failed.append(file)
    
    if failed:
        print(f"\n❌ Missing files: {', '.join(failed)}")
        return False
    else:
        print("\n✅ All required files exist!")
        return True

def test_data_generation():
    """Test if data can be generated"""
    print("\nTesting data generation...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Simple test data generation
        np.random.seed(42)
        test_data = pd.DataFrame({
            'area': np.random.normal(1800, 500, 10),
            'bedrooms': np.random.randint(1, 6, 10),
            'bathrooms': np.random.choice([1, 2, 3], 10),
            'age': np.random.exponential(15, 10),
            'location_score': np.random.uniform(1, 10, 10),
            'price': np.random.normal(400000, 100000, 10)
        })
        
        print(f"  ✓ Generated test data: {test_data.shape}")
        print("\n✅ Data generation works!")
        return True
        
    except Exception as e:
        print(f"\n❌ Data generation failed: {e}")
        return False

def test_model_training():
    """Test if model training works"""
    print("\nTesting model training capability...")
    
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split
        import numpy as np
        
        # Create simple test data
        X = np.random.rand(100, 5)
        y = np.random.rand(100)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        
        print(f"  ✓ Model trained successfully (R² = {score:.4f})")
        print("\n✅ Model training works!")
        return True
        
    except Exception as e:
        print(f"\n❌ Model training failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("HOUSE PRICE PREDICTION - SYSTEM TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Package Imports", test_imports()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Required Files", test_files()))
    results.append(("Data Generation", test_data_generation()))
    results.append(("Model Training", test_model_training()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nYou're ready to run the pipeline:")
        print("  1. python data/generate_data.py")
        print("  2. python run_pipeline.py")
        print("  3. cd app && python app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before proceeding.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
