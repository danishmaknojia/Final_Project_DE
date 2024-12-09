import os
import kagglehub
import boto3
from botocore.exceptions import NoCredentialsError

# S3 bucket configuration
S3_BUCKET_NAME = "cbb-data-engg"
S3_FOLDER = "Final_Project_DE/archive"
AWS_REGION = "us-west-2"

# Kaggle dataset configuration
DATASET_NAME = "andrewsundberg/college-basketball-dataset"

def upload_to_s3(file_path, bucket, s3_key):
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    try:
        s3_client.upload_file(file_path, bucket, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket}/{s3_key}")
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except NoCredentialsError:
        print("Error: AWS credentials not available")

def main():
    # Download the dataset using kagglehub
    print("Downloading dataset...")
    dataset_path = kagglehub.dataset_download(DATASET_NAME)
    print(f"Path to dataset files: {dataset_path}")
    
    # Iterate over downloaded files and upload to S3
    for root, _, files in os.walk(dataset_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            s3_key = os.path.join(S3_FOLDER, file_name)
            upload_to_s3(local_file_path, S3_BUCKET_NAME, s3_key)

if __name__ == "__main__":
    main()
