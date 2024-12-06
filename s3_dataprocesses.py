import pandas as pd
import logging
import boto3
from io import StringIO

# Set up logging
logging.basicConfig(
    filename="data_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# S3 Configuration
s3 = boto3.client("s3")
bucket_name = "cbb-data-engg"
input_prefix = "Final_Project_DE/archive/"
output_prefix = "Final_Project_DE/"


def upload_to_s3(local_path, bucket, s3_key):
    """Upload a local file to S3."""
    try:
        s3.upload_file(local_path, bucket, s3_key)
        logging.info(f"Uploaded {local_path} to S3 as {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading {local_path} to S3: {e}")
        raise


def read_s3_csv(bucket, key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))
    except Exception as e:
        logging.error(f"Error reading {key} from S3: {e}")
        raise


def write_s3_csv(df, bucket, key):
    """Write a Pandas DataFrame to S3 as a CSV file."""
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    except Exception as e:
        logging.error(f"Error writing {key} to S3: {e}")
        raise


# Step 1: Upload local files to S3
local_folder = "../Final_Project_DE/archive"
files_to_upload = [
    "cbb22.csv",
    "cbb22.csv",
    "cbb22.csv",
    "cbb22.csv",
    "cbb16.csv",
    "cbb.csv",
    "cbb24.csv",  # Add all necessary files here
]

for file_name in files_to_upload:
    local_file_path = f"{local_folder}/{file_name}"
    s3_key = f"{input_prefix}{file_name}"  # Define the S3 key for the file
    upload_to_s3(local_file_path, bucket_name, s3_key)

# Step 2: Process files on S3
logging.info("Processing cbb22.csv.")
df_22 = read_s3_csv(bucket_name, f"{input_prefix}cbb22.csv")
df_22.rename(columns={"EFGD_D": "EFG_D"}, inplace=True)
write_s3_csv(df_22, bucket_name, f"{input_prefix}cbb22.csv")

# Process cbb16.csv and cbb.csv
logging.info("Processing cbb16.csv and cbb.csv.")
df_16 = read_s3_csv(bucket_name, f"{input_prefix}cbb16.csv")
df_all = read_s3_csv(bucket_name, f"{input_prefix}cbb.csv")

logging.info("Filtering rows for the year 2016 in cbb.csv.")
df_all_16 = df_all[df_all["YEAR"] == 2016]

logging.info(
    "Merging cbb16.csv with filtered cbb.csv for 'POSTSEASON' and 'SEED' columns."
)
df_16 = pd.merge(
    df_16, df_all_16[["TEAM", "POSTSEASON", "SEED"]], on="TEAM", how="left"
)

logging.info("Combining and cleaning 'POSTSEASON' and 'SEED' columns in cbb16.csv.")
df_16["POSTSEASON"] = df_16["POSTSEASON_x"].combine_first(df_16["POSTSEASON_y"])
df_16["SEED"] = df_16["SEED_x"].combine_first(df_16["SEED_y"])
df_16.drop(columns=["POSTSEASON_x", "POSTSEASON_y", "SEED_x", "SEED_y"], inplace=True)

write_s3_csv(df_16, bucket_name, f"{input_prefix}cbb16.csv")

# Combine multiple CSV files from S3
logging.info("Combining multiple CSV files.")
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=input_prefix)
csv_files = [
    obj["Key"]
    for obj in response.get("Contents", [])
    if obj["Key"].endswith(".csv")
    and obj["Key"]
    not in [
        f"{input_prefix}cbb.csv",
        f"{input_prefix}cbb24.csv",
        f"{input_prefix}cbb20.csv",
    ]
]

dataframes = []

for file_key in csv_files:
    try:
        logging.info(f"Reading {file_key} from S3.")
        df = read_s3_csv(bucket_name, file_key)
        dataframes.append(df)
    except Exception as e:
        logging.error(f"Error reading {file_key}: {e}")

combined_df = pd.concat(dataframes, ignore_index=True)
write_s3_csv(combined_df, bucket_name, f"{output_prefix}combined_cbb.csv")

# Process cbb24.csv
logging.info("Processing cbb24.csv.")
cbb24 = read_s3_csv(bucket_name, f"{input_prefix}cbb24.csv")
cbb24["EFG_O"] = cbb24["EFG%"]
cbb24["EFG_D"] = cbb24["EFGD%"]
cbb24 = cbb24[
    [
        "TEAM",
        "CONF",
        "G",
        "W",
        "ADJOE",
        "ADJDE",
        "BARTHAG",
        "EFG_O",
        "EFG_D",
        "TOR",
        "TORD",
        "ORB",
        "DRB",
        "FTR",
        "FTRD",
        "2P_O",
        "2P_D",
        "3P_O",
        "3P_D",
        "ADJ_T",
        "WAB",
        "SEED",
    ]
]

write_s3_csv(combined_df, bucket_name, f"{output_prefix}train_data.csv")
write_s3_csv(cbb24, bucket_name, f"{output_prefix}test_data.csv")

logging.info("Processing completed successfully.")
