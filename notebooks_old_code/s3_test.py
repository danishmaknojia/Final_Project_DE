import boto3
import pandas as pd
from read_write_files_s3 import write_s3_csv, read_s3_csv

# S3 Configuration
bucket_name = "cbb-data-engg"
test_key = "test.csv"
s3 = boto3.client("s3")

# Files that should exist on s3 (we want to check if they are there)
expected_files = [
    "Final_Project_DE/current_cbb_live_data.csv",
    "Final_Project_DE/archive/cbb22.csv",
    "Final_Project_DE/archive/cbb16.csv",
    "Final_Project_DE/archive/cbb.csv",
    "Final_Project_DE/archive/cbb24.csv",
    "Final_Project_DE/combined_cbb.csv",
    "Final_Project_DE/train_data.csv",
    "Final_Project_DE/test_data.csv",
]


def file_exists_in_s3(bucket, key):
    """Check if a file exists in S3."""
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False


def test_created_files_exist_in_s3():
    """Test that all expected files exist on S3."""
    missing_files = []
    for file_key in expected_files:
        if not file_exists_in_s3(bucket_name, file_key):
            missing_files.append(file_key)

    assert (
        not missing_files
    ), f"The following files are missing from S3: {missing_files}"

    print("Test passed: All expected files exist on S3.")


def test_write_s3_csv():
    """Test the write_s3_csv function."""
    # Creating a file to write
    sample_df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["A", "B", "C"]})

    write_s3_csv(sample_df, bucket_name, test_key)

    # Check content
    try:
        response = s3.get_object(Bucket=bucket_name, Key=test_key)
        file_content = response["Body"].read().decode("utf-8")
        print(f"File content of {test_key}: {file_content}")
    except s3.exceptions.ClientError as e:
        print(f"Error getting the file: {e}")

    # Check file exist in cbb-data-engg on s3
    assert file_exists_in_s3(bucket_name, test_key), "Test file was not found in S3."

    #  Read the file back and ensure it's correct
    read_df = read_s3_csv(bucket_name, test_key)
    assert not read_df.empty, "The test file in S3 is empty."

    # Verify that the data matches the sample data
    pd.testing.assert_frame_equal(sample_df, read_df, check_dtype=True)

    print("Test passed: `write_s3_csv` works as expected.")


# Run the test
if __name__ == "__main__":
    test_created_files_exist_in_s3()
    test_write_s3_csv()
