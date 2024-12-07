import numpy as np
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(
    filename="data_processing_local.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def rename_column_in_file(file_path, column_mapping):
    """Rename columns in a CSV file and save the updated file."""
    try:
        logging.info(f"Reading {file_path}.")
        df = pd.read_csv(file_path)
        df.rename(columns=column_mapping, inplace=True)
        df.to_csv(file_path, index=False)
        logging.info(f"Renamed columns and saved updated {file_path}.")
    except Exception as e:
        logging.error(f"Error renaming columns in {file_path}: {e}")


def merge_postseason_and_seed(cbb_file, cbb16_file):
    """Merge postseason and seed data from cbb.csv into cbb16.csv."""
    try:
        logging.info(f"Reading {cbb_file} and {cbb16_file}.")
        df_all = pd.read_csv(cbb_file)
        df_16 = pd.read_csv(cbb16_file)

        logging.info("Filtering rows for the year 2016 in cbb.csv.")
        df_all_16 = df_all[df_all["YEAR"] == 2016]

        logging.info("Merging postseason and seed columns into cbb16.csv.")
        df_16 = pd.merge(
            df_16, df_all_16[["TEAM", "POSTSEASON", "SEED"]], on="TEAM", how="left"
        )

        logging.info("Combining 'POSTSEASON' and 'SEED' columns.")
        df_16["POSTSEASON"] = df_16["POSTSEASON_x"].combine_first(df_16["POSTSEASON_y"])
        df_16["SEED"] = df_16["SEED_x"].combine_first(df_16["SEED_y"])

        df_16.drop(
            columns=["POSTSEASON_x", "POSTSEASON_y", "SEED_x", "SEED_y"], inplace=True
        )
        df_16.to_csv(cbb16_file, index=False)
        logging.info(f"Saved updated {cbb16_file}.")
    except Exception as e:
        logging.error(f"Error merging postseason and seed data: {e}")


def combine_csv_files(input_folder, exclude_files, output_file):
    """Combine multiple CSV files into one, excluding specific files."""
    try:
        logging.info(f"Combining CSV files in {input_folder}.")
        csv_files = [
            os.path.join(input_folder, file)
            for file in os.listdir(input_folder)
            if file.endswith(".csv") and file not in exclude_files
        ]

        dataframes = []
        for csv_file in csv_files:
            try:
                logging.info(f"Reading {csv_file}.")
                df = pd.read_csv(csv_file)
                dataframes.append(df)
            except Exception as e:
                logging.error(f"Error reading {csv_file}: {e}")

        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        logging.info(f"Saved combined data to {output_file}.")
        return combined_df
    except Exception as e:
        logging.error(f"Error combining CSV files: {e}")


def process_cbb24(cbb24_file):
    """Process cbb24.csv and create a test dataset."""
    try:
        logging.info(f"Processing {cbb24_file}.")
        cbb24 = pd.read_csv(cbb24_file)
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
        cbb24.to_csv("test_data.csv", index=False)
        logging.info("Saved test_data.csv.")
    except Exception as e:
        logging.error(f"Error processing {cbb24_file}: {e}")


def main():
    # Step 1: Rename column in cbb22.csv
    rename_column_in_file("../Final_Project_DE/archive/cbb22.csv", {"EFGD_D": "EFG_D"})

    # Step 2: Merge postseason and seed data into cbb16.csv
    merge_postseason_and_seed(
        "../Final_Project_DE/archive/cbb.csv", "../Final_Project_DE/archive/cbb16.csv"
    )

    # Step 3: Combine all CSV files except exclusions
    combined_df = combine_csv_files(
        "../Final_Project_DE/archive",
        ["cbb.csv", "cbb24.csv", "cbb20.csv"],
        "train_data.csv",
    )

    # Step 4: Process cbb24.csv
    process_cbb24("../Final_Project_DE/archive/cbb24.csv")


if __name__ == "__main__":
    main()
