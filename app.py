from flask import Flask, render_template
from mylib.functions import loadTeams, extractSeeds, extractFirstLastRanks, extractConferences
from mylib.functions import finalFour, teamStats
from mylib.lib import read_s3_csv
from datetime import datetime
import pytz
import boto3
import logging
        
# Initialize the Flask application
app = Flask(__name__)

# with open("read_write_files_s3.py") as f: 
#     exec(f.read())
# with open("final_model.py") as f: 
#     exec(f.read())

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more verbose logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Logs to a file named app.log
        logging.StreamHandler()          # Logs to the console
    ]
)

# Log app start
logging.info("Initializing March Madness Predictor Flask application.")

# Load and process data

s3 = boto3.client("s3")
bucket_name = "cbb-data-engg"
output_prefix = "Final_Project_DE/"
current_date = datetime.now().strftime("%Y%m%d")
file_name_final = f"cbb25_seeded_{current_date}.csv"



# Page 2


@app.route("/")
def index():
    try:
        # Get current time in Eastern Time (ET)
        eastern = pytz.timezone("US/Eastern")
        last_updated = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p")
        
        logging.info(f"Loading data from {output_prefix}{file_name_final}")
        df = read_s3_csv(bucket_name, f"{output_prefix}{file_name_final}")
        dfClean = loadTeams(df)
        dfGroupSeed = extractSeeds(dfClean)
        dfFirstLastRanks = extractFirstLastRanks(dfClean)
        dfGroupConference = extractConferences(dfClean)
        logging.info("Data loaded and processed successfully.")
        
        logging.info("Rendering index page.")
        
        # Pass data and description to the template
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
def final_four():
    try:
        df = read_s3_csv(bucket_name, f"{output_prefix}{file_name_final}")
        dfClean = loadTeams(df)
        logging.info("Predicting Final Four results.")
        Top4 = finalFour(dfClean)  # Predict Final Four results
        logging.info(f"Final Four prediction completed: {Top4}")
        logging.info("Rendering Final Four page.")
        team_stats = teamStats(df, Top4)
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

@app.route('/health')
def health_check():
    # Add logic to check dependencies (e.g., database, cache)
    return "Healthy", 200

if __name__ == "__main__":
    logging.info("Starting Flask application.")
    app.run(host="0.0.0.0", port=8080)


