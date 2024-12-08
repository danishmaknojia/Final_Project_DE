from flask import Flask, render_template
from mylib.functions import loadCSV, loadTeams, extractSeeds, extractFirstLastRanks, extractConferences
from mylib.functions import finalFour, teamStats
from datetime import datetime
import pytz
import os
import logging
        
# Initialize the Flask application
app = Flask(__name__)

with open("read_write_files_s3.py") as f: 
    exec(f.read())
with open("final_model.py") as f: 
    exec(f.read())

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more verbose logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file named app.log
        logging.StreamHandler()          # Logs to the console
    ]
)

# Log app start
logging.info("Initializing March Madness Predictor Flask application.")

# Load and process data
filePath = "cbb25_seeded_20241122.csv"
if not os.path.exists(filePath):
    logging.error(f"Data file not found: {filePath}")
    raise FileNotFoundError(f"Data file not found: {filePath}")

logging.info(f"Loading data from {filePath}")
df = loadCSV(filePath)
dfClean = loadTeams(df)
dfGroupSeed = extractSeeds(dfClean)
dfFirstLastRanks = extractFirstLastRanks(dfClean)
dfGroupConference = extractConferences(dfClean)
logging.info("Data loaded and processed successfully.")

# Page 2
logging.info("Predicting Final Four results.")
Top4 = finalFour(dfClean)  # Predict Final Four results
logging.info(f"Final Four prediction completed: {Top4}")

@app.route("/")
def index():
    try:
        # Get current time in Eastern Time (ET)
        eastern = pytz.timezone("US/Eastern")
        last_updated = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p")
        
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


