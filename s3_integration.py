"""
AWS S3 Integration for House Price Prediction
Upload/Download models and data to/from S3
"""
import boto3
import os
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, bucket_name):
        """Initialize S3 client"""
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def create_bucket(self, region='us-east-1'):
        """Create S3 bucket if it doesn't exist"""
        try:
            if region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"✓ Bucket '{self.bucket_name}' created successfully")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"✓ Bucket '{self.bucket_name}' already exists")
            else:
                print(f"✗ Error creating bucket: {e}")
    
    def upload_file(self, local_path, s3_key):
        """Upload file to S3"""
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            print(f"✓ Uploaded: {local_path} → s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            print(f"✗ Error uploading {local_path}: {e}")
            return False
    
    def download_file(self, s3_key, local_path):
        """Download file from S3"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            print(f"✓ Downloaded: s3://{self.bucket_name}/{s3_key} → {local_path}")
            return True
        except ClientError as e:
            print(f"✗ Error downloading {s3_key}: {e}")
            return False
    
    def upload_model_artifacts(self):
        """Upload all model artifacts to S3"""
        print("\n" + "=" * 50)
        print("UPLOADING MODEL ARTIFACTS TO S3")
        print("=" * 50)
        
        artifacts = [
            ('models/house_price_model.pkl', 'models/house_price_model.pkl'),
            ('models/scaler.pkl', 'models/scaler.pkl'),
            ('models/feature_names.pkl', 'models/feature_names.pkl'),
            ('data/processed/engineered_data.csv', 'data/engineered_data.csv')
        ]
        
        for local_path, s3_key in artifacts:
            if os.path.exists(local_path):
                self.upload_file(local_path, s3_key)
            else:
                print(f"⚠ File not found: {local_path}")
    
    def download_model_artifacts(self):
        """Download all model artifacts from S3"""
        print("\n" + "=" * 50)
        print("DOWNLOADING MODEL ARTIFACTS FROM S3")
        print("=" * 50)
        
        artifacts = [
            ('models/house_price_model.pkl', 'models/house_price_model.pkl'),
            ('models/scaler.pkl', 'models/scaler.pkl'),
            ('models/feature_names.pkl', 'models/feature_names.pkl')
        ]
        
        for s3_key, local_path in artifacts:
            self.download_file(s3_key, local_path)

def main():
    """Main function for S3 operations"""
    import sys
    
    # Configuration
    BUCKET_NAME = 'house-price-prediction-models'  # Change this to your bucket name
    
    s3_manager = S3Manager(BUCKET_NAME)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python s3_integration.py upload   - Upload models to S3")
        print("  python s3_integration.py download - Download models from S3")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'upload':
        s3_manager.create_bucket()
        s3_manager.upload_model_artifacts()
        print("\n✓ All artifacts uploaded successfully!")
        
    elif command == 'download':
        s3_manager.download_model_artifacts()
        print("\n✓ All artifacts downloaded successfully!")
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
