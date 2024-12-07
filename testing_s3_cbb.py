import hashlib
import pandas as pd
import logging
import boto3
from io import StringIO

# Set up logging
logging.basicConfig(
    filename="data_verification.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# S3 Configuration
s3 = boto3.client("s3")
bucket_name = "cbb-data-engg"
input_prefix = "Final_Project_DE/"
local_files_s3_keys = {
    "../Final_Project_DE/train_data.csv": f"{input_prefix}train_data.csv",
    "../Final_Project_DE/test_data.csv": f"{input_prefix}test_data.csv",
    "../Final_Project_DE/current_cbb_live_data.csv": f"{input_prefix}current_cbb_live_data.csv",
}


def calculate_md5(file_path):
    """Calculate the MD5 hash of a local file."""
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating MD5 for {file_path}: {e}")
        raise


def calculate_s3_md5(bucket, key):
    """Calculate the MD5 hash of an S3 object."""
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: obj["Body"].read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating MD5 for S3 object {key}: {e}")
        raise


def verify_files(local_path, bucket, key):
    """Compare the MD5 hashes of a local file and an S3 object."""
    try:
        local_md5 = calculate_md5(local_path)
        s3_md5 = calculate_s3_md5(bucket, key)
        if local_md5 == s3_md5:
            logging.info(f"{local_path} and {key} are identical.")
            print(f"{local_path} and {key} are identical.")
        else:
            logging.warning(f"{local_path} and {key} differ.")
            print(f"{local_path} and {key} differ.")
    except Exception as e:
        logging.error(f"Error verifying {local_path} and {key}: {e}")
        print(f"Error verifying {local_path} and {key}: {e}")


if __name__ == "__main__":
    for local_file, s3_key in local_files_s3_keys.items():
        print(f"Verifying {local_file} against S3 key {s3_key}...")
        verify_files(local_file, bucket_name, s3_key)
