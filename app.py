from flask import Flask, render_template
from mylib.functions import loadTeams, extractSeeds, extractFirstLastRanks, extractConferences, finalFour, teamStats
from mylib.lib import read_s3_csv
from datetime import datetime
import pytz
import boto3
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Use logging.DEBUG for verbose logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Logs to a file
        logging.StreamHandler()              # Logs to the console
    ]
)

with open("read_write_files_s3.py") as f: 
    exec(f.read())
with open("final_model.py") as f: 
    exec(f.read())

# Log app initialization
logging.info("Initializing March Madness Predictor Flask application.")

# AWS S3 configuration
s3 = boto3.client("s3")
bucket_name = "cbb-data-engg"
output_prefix = "Final_Project_DE/"
current_date = datetime.now().strftime("%Y%m%d")
file_name_final = f"cbb25_seeded_{current_date}.csv"

# Helper function to load and process data
def load_and_process_data():
    """
    Fetches data from S3 and processes it for analysis.
    Returns processed dataframes and other relevant results.
    """
    try:

        with open("read_write_files_s3.py") as f: 
            exec(f.read())
        with open("final_model.py") as f: 
            exec(f.read())
        logging.info(f"Loading data from S3: {output_prefix}{file_name_final}")
        df = read_s3_csv(bucket_name, f"{output_prefix}{file_name_final}")
        
        # Process data
        dfClean = loadTeams(df)
        dfGroupSeed = extractSeeds(dfClean)
        dfFirstLastRanks = extractFirstLastRanks(dfClean)
        dfGroupConference = extractConferences(dfClean)
        logging.info("Data loaded and processed successfully.")
        
        return df, dfClean, dfGroupSeed, dfFirstLastRanks, dfGroupConference
    except Exception as e:
        logging.error(f"Error during data processing: {e}")
        raise


@app.route("/")
def index():
    """
    Renders the index page with team rankings, seed groupings, and conference breakdowns.
    """
    try:
        # Get current time in Eastern Time (ET)
        eastern = pytz.timezone("US/Eastern")
        last_updated = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p")
        
        # Load and process data
        _, _, dfGroupSeed, dfFirstLastRanks, dfGroupConference = load_and_process_data()

        logging.info("Rendering index page.")
        return render_template(
            "index.html",
            last_updated=last_updated,
            group_name="March Madness 2024",
            first_team=dfFirstLastRanks[0],
            second_to_last_team=dfFirstLastRanks[1],
            last_team=dfFirstLastRanks[2],
            grouped_seeds=dfGroupSeed,
            grouped_conferences=dfGroupConference,
            description=(
                "Welcome to the March Madness Predictor! This tool provides a detailed overview of team rankings, "
                "seed groupings, and conference breakdowns for the 2024 season. Use the insights to stay ahead in your brackets!"
            ),
        )
    except Exception as e:
        logging.error(f"Error rendering index page: {e}")
        return "An error occurred. Please check the logs for details.", 500


@app.route("/final_four")
def final_four_route():
    """
    Renders the Final Four predictions page with team stats and predictions.
    """
    try:
        # Load and process data
        df, dfClean, _, _, _ = load_and_process_data()

        # Predict Final Four results
        logging.info("Predicting Final Four results.")
        Top4 = finalFour(dfClean)
        logging.info(f"Final Four prediction completed: {Top4}")

        # Calculate team statistics
        team_stats = teamStats(df, Top4)
        logging.info("Rendering Final Four page.")
        return render_template(
            "final_four.html",
            winner=Top4["winner"],
            runner_up=Top4["runner_up"],
            final_four=Top4["final_four"],
            team_stats=team_stats
        )
    except Exception as e:
        logging.error(f"Error rendering Final Four page: {e}")
        return "An error occurred. Please check the logs for details.", 500


@app.route("/health")
def health_check():
    """
    Simple health check endpoint to verify application status.
    """
    try:
        # Example: Check S3 connectivity or file existence
        s3.head_object(Bucket=bucket_name, Key=f"{output_prefix}{file_name_final}")
        logging.info("Health check passed.")
        return "Healthy", 200
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return "Unhealthy", 500


if __name__ == "__main__":
    logging.info("Starting Flask application.")
    app.run(host="0.0.0.0", port=8080)