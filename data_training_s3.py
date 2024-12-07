import pandas as pd
import logging
import boto3
from io import StringIO

# Configure logging
logging.basicConfig(
    filename="data_processing_s3.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize S3 client
s3_client = boto3.client("s3")
bucket_name = "cbb-data-engg"
input_folder = "Final_Project_DE/archive/"
output_folder = "Final_Project_DE/"
input_file = f"{input_folder}cbb.csv"
output_file = f"{output_folder}train_data.csv"
local_file_path = "../Final_Project_DE/train_data.csv"  # Update with your local path


def read_s3_csv(bucket, key):
    """Read a CSV file from S3."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(response["Body"])
    except Exception as e:
        logging.error(f"Error reading {key} from S3: {e}")
        raise


def save_s3_csv(df, bucket, key):
    """Save a DataFrame as a CSV file to S3."""
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        logging.info(f"Saved {key} to S3.")
    except Exception as e:
        logging.error(f"Error saving {key} to S3: {e}")
        raise


def upload_file_to_s3(bucket_name, s3_key, local_file_path):
    """Upload a local file to S3."""
    try:
        logging.info(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        logging.info(f"Successfully uploaded to s3://{bucket_name}/{s3_key}")
        print(f"File uploaded successfully to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
        print(f"Error uploading file to S3: {e}")


def process_cbb_to_train_data(input_bucket, input_key, output_bucket, output_key):
    """Copy cbb.csv from input to train_data.csv output."""
    try:
        logging.info(f"Processing {input_key} into {output_key}.")
        df = read_s3_csv(input_bucket, input_key)
        save_s3_csv(df, output_bucket, output_key)
        logging.info(f"Successfully processed {input_key} into {output_key}.")
    except Exception as e:
        logging.error(f"Error processing {input_key}: {e}")


def main():
    # Process and save the train_data.csv to S3
    process_cbb_to_train_data(bucket_name, input_file, bucket_name, output_file)

    # Upload the train_data.csv from the local directory to S3
    upload_file_to_s3(bucket_name, output_file, local_file_path)


if __name__ == "__main__":
    main()


# Initialize S3 client
s3_client = boto3.client("s3")
bucket_name = "cbb-data-engg"
input_folder = "Final_Project_DE/archive/"
output_folder = "Final_Project_DE/"
input_cbb24_file = f"{input_folder}cbb24.csv"
output_test_file = f"{output_folder}test_data.csv"


def read_s3_csv(bucket, key):
    """Read a CSV file from S3."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(response["Body"])
    except Exception as e:
        logging.error(f"Error reading {key} from S3: {e}")
        raise


def save_s3_csv(df, bucket, key):
    """Save a DataFrame as a CSV file to S3."""
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        logging.info(f"Saved {key} to S3.")
    except Exception as e:
        logging.error(f"Error saving {key} to S3: {e}")
        raise


def process_test_data(input_bucket, input_key, output_bucket, output_key):
    """Process cbb24.csv from S3 and create a test dataset."""
    try:
        logging.info(f"Processing {input_key} to generate test dataset.")
        df = read_s3_csv(input_bucket, input_key)
        df["EFG_O"] = df["EFG%"]
        df["EFG_D"] = df["EFGD%"]
        df = df[
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

        # Save the processed DataFrame to S3
        save_s3_csv(df, output_bucket, output_key)
        logging.info(f"Successfully processed and uploaded {output_key} to S3.")
    except Exception as e:
        logging.error(f"Error processing {input_key}: {e}")


def main():
    # Process the test dataset from S3 and upload to S3
    process_test_data(bucket_name, input_cbb24_file, bucket_name, output_test_file)


if __name__ == "__main__":
    main()


# import pandas as pd
# import boto3
# from io import StringIO

# # Initialize S3 client
# s3 = boto3.client("s3")
# bucket_name = "cbb-data-engg"
# input_prefix = "Final_Project_DE/archive/"
# output_key = "Final_Project_DE/train_data.csv"


# def read_csv_from_s3(bucket_name, file_key):
#     try:
#         response = s3.get_object(Bucket=bucket_name, Key=file_key)
#         df = pd.read_csv(response["Body"])
#         return df
#     except Exception as e:
#         print(f"Error reading {file_key}: {e}")
#         return None


# def save_to_s3(df, bucket_name, output_key):
#     try:
#         csv_buffer = StringIO()
#         df.to_csv(csv_buffer, index=False)
#         csv_buffer.seek(0)
#         s3.put_object(Bucket=bucket_name, Key=output_key, Body=csv_buffer.getvalue())
#         print(f"Successfully saved the file to s3://{bucket_name}/{output_key}")
#     except Exception as e:
#         print(f"Error saving file to S3: {e}")


# # Example: Read files
# cbb22_df = read_csv_from_s3(bucket_name, f"{input_prefix}cbb22.csv")
# cbb_csv = read_csv_from_s3(bucket_name, f"{input_prefix}cbb.csv")
# cbb16_df = read_csv_from_s3(bucket_name, f"{input_prefix}cbb16.csv")

# # Example: Combine data (you can add your logic here)
# if cbb22_df is not None and cbb_csv is not None and cbb16_df is not None:
#     combined_df = pd.concat([cbb22_df, cbb_csv, cbb16_df], ignore_index=True)

#     # Save combined data to S3
#     save_to_s3(combined_df, bucket_name, output_key)


# import numpy as np
# import pandas as pd
# import logging
# import io
# import boto3

# # Configure logging
# logging.basicConfig(
#     filename="data_processing_s3_cleaning.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# # S3 Configuration
# s3 = boto3.client("s3")
# bucket_name = "cbb-data-engg"
# input_prefix = "Final_Project_DE/archive/"
# output_key = "Final_Project_DE/train_data.csv"

# # List of S3 keys to be processed
# exclude_files = ["cbb.csv", "cbb24.csv", "cbb20.csv"]


# def read_csv_from_s3(s3_key):
#     """Read CSV file from S3 and return as DataFrame."""
#     try:
#         logging.info(f"Reading {s3_key} from S3.")
#         obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
#         df = pd.read_csv(io.BytesIO(obj["Body"].read()))
#         logging.info(
#             f"Successfully read {s3_key} from S3. DataFrame shape: {df.shape}."
#         )
#         return df
#     except Exception as e:
#         logging.error(f"Error reading {s3_key} from S3: {e}")
#         raise


# def combine_csv_files_from_s3(input_prefix, exclude_files):
#     """Combine all CSV files from S3 into one, excluding specific files."""
#     try:
#         logging.info(f"Combining CSV files from S3 in {input_prefix}.")
#         dataframes = []

#         # List all objects in the S3 folder
#         result = s3.list_objects_v2(Bucket=bucket_name, Prefix=input_prefix)

#         # Filter files that are CSV and not in the exclude list
#         csv_files = [
#             obj["Key"]
#             for obj in result.get("Contents", [])
#             if obj["Key"].endswith(".csv")
#             and obj["Key"].split("/")[-1] not in exclude_files
#         ]

#         # Read and append each CSV file to the list of DataFrames
#         for s3_key in csv_files:
#             df = read_csv_from_s3(s3_key)
#             if df.empty:
#                 logging.warning(f"{s3_key} is empty, skipping.")
#             else:
#                 dataframes.append(df)

#         if dataframes:
#             combined_df = pd.concat(dataframes, ignore_index=True)
#             logging.info(
#                 f"Successfully combined CSV files. Combined DataFrame shape: {combined_df.shape}."
#             )
#             return combined_df
#         else:
#             logging.error("No data frames to combine.")
#             return pd.DataFrame()  # Return empty DataFrame if none were added

#     except Exception as e:
#         logging.error(f"Error combining CSV files from S3: {e}")
#         raise


# def save_df_to_s3(df, s3_key):
#     """Save DataFrame to S3 as a CSV file."""
#     try:
#         logging.info(f"Saving DataFrame to S3 as {s3_key}.")
#         csv_buffer = io.StringIO()
#         df.to_csv(csv_buffer, index=False)
#         s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
#         logging.info(f"Successfully saved {s3_key} to S3.")
#     except Exception as e:
#         logging.error(f"Error saving {s3_key} to S3: {e}")
#         raise


# def main():
#     try:
#         # Step 1: Combine all CSV files from the S3 folder except exclusions
#         combined_df = combine_csv_files_from_s3(input_prefix, exclude_files)

#         if combined_df.empty:
#             logging.error("No data was combined. Please check the individual files.")
#         else:
#             # Step 2: Save the combined DataFrame to S3
#             logging.info("Saving combined data to S3.")
#             save_df_to_s3(combined_df, output_key)

#         logging.info("All steps completed successfully.")
#     except Exception as e:
#         logging.error(f"Error in processing: {e}")


# if __name__ == "__main__":
#     main()
