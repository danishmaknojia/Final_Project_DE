import pandas as pd
import logging
import boto3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from mylib.lib import upload_to_s3, read_s3_csv, write_s3_csv, extract_bart_torvik_data

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


def write_s3_csv(df, bucket, key):
    """Write a Pandas DataFrame to S3 as a CSV file."""
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        logging.info(f"Uploaded DataFrame to S3 as {key}.")
    except Exception as e:
        logging.error(f"Error writing {key} to S3: {e}")
        raise


def read_s3_csv(bucket, key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))
    except Exception as e:
        logging.error(f"Error reading {key} from S3: {e}")
        raise


def upload_to_s3(local_path, bucket, s3_key):
    """Upload a local file to S3."""
    try:
        s3.upload_file(local_path, bucket, s3_key)
        logging.info(f"Uploaded {local_path} to S3 as {s3_key}.")
    except Exception as e:
        logging.error(f"Error uploading {local_path} to S3: {e}")
        raise


def extract_bart_torvik_data():
    """Extract, transform, and upload Bart Torvik data to S3."""
    logging.info("Extracting data from Bart Torvik.")
    url = "https://www.barttorvik.com/"
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    # Convert to DataFrame and transform
    df = pd.DataFrame(data)
    df = df.dropna(how="all").reset_index(drop=True)

    df.columns = [
        "RK",
        "TEAM",
        "CONF",
        "G",
        "REC",
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
        "3PR",
        "3PRD",
        "ADJ_T",
        "WAB",
    ]
    df = df[
        [
            "TEAM",
            "CONF",
            "G",
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
        ]
    ]

    # Define S3 key and upload
    s3_key = f"{output_prefix}current_cbb_live_data.csv"
    write_s3_csv(df, bucket_name, s3_key)
    logging.info("Bart Torvik data extraction and upload completed.")


def process_local_files():
    """Upload and process local files."""
    local_folder = "../Final_Project_DE/archive"
    files_to_upload = ["cbb22.csv", "cbb16.csv", "cbb.csv", "cbb24.csv"]

    for file_name in files_to_upload:
        local_file_path = f"{local_folder}/{file_name}"
        s3_key = f"{input_prefix}{file_name}"
        upload_to_s3(local_file_path, bucket_name, s3_key)


def process_s3_files():
    """Process files stored in S3."""
    logging.info("Processing cbb22.csv.")
    df_22 = read_s3_csv(bucket_name, f"{input_prefix}cbb22.csv")
    df_22.rename(columns={"EFGD_D": "EFG_D"}, inplace=True)
    write_s3_csv(df_22, bucket_name, f"{input_prefix}cbb22.csv")

    logging.info("Processing cbb16.csv and cbb.csv.")
    df_16 = read_s3_csv(bucket_name, f"{input_prefix}cbb16.csv")
    df_all = read_s3_csv(bucket_name, f"{input_prefix}cbb.csv")

    df_all_16 = df_all[df_all["YEAR"] == 2016]
    df_16 = pd.merge(
        df_16, df_all_16[["TEAM", "POSTSEASON", "SEED"]], on="TEAM", how="left"
    )
    df_16["POSTSEASON"] = df_16["POSTSEASON_x"].combine_first(df_16["POSTSEASON_y"])
    df_16["SEED"] = df_16["SEED_x"].combine_first(df_16["SEED_y"])
    df_16.drop(
        columns=["POSTSEASON_x", "POSTSEASON_y", "SEED_x", "SEED_y"], inplace=True
    )

    write_s3_csv(df_16, bucket_name, f"{input_prefix}cbb16.csv")

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

    dataframes = [read_s3_csv(bucket_name, file_key) for file_key in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    write_s3_csv(combined_df, bucket_name, f"{output_prefix}combined_cbb.csv")

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


if __name__ == "__main__":
    extract_bart_torvik_data()
    process_local_files()
    process_s3_files()
    logging.info("All tasks completed successfully.")
