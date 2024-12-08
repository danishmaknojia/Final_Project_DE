import os
import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a session using Amazon S3
s3 = boto3.client('s3')
bucket_name = "cbb-data-engg"

# Directory to save downloaded files
local_file_path = 'pulled_files/'

# Ensure the local directory exists
if not os.path.exists(local_file_path):
    os.makedirs(local_file_path)

# List and download files
try:
    files = []
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            file_key = obj['Key']
            logging.info(f"Found file: {file_key}")
            files.append(file_key)

            # Ensure the local file path preserves folder structure
            local_path = os.path.join(local_file_path, file_key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download the file
            logging.info(f"Downloading {file_key} to {local_path}")
            s3.download_file(bucket_name, file_key, local_path)
    else:
        logging.warning("No files found in the S3 bucket.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
