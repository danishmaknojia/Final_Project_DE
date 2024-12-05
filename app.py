from flask import Flask, render_template
from functions import loadCSV, loadTeams, extractSeeds, extractFirstLastRanks, extractConferences
from functions import finalFour, teamStats
from datetime import datetime
import pytz
import os

app = Flask(__name__)

# Load and process data
filePath = "cbb25_seeded_20241122.csv"
df = loadCSV(filePath)
dfClean = loadTeams(df)
dfGroupSeed = extractSeeds(dfClean)
dfFirstLastRanks = extractFirstLastRanks(dfClean)
dfGroupConference = extractConferences(dfClean)

# Page 2
Top4 = finalFour(dfClean)  # Predict Final Four results

@app.route("/")
def index():
    # Get current time in Eastern Time (ET)
    eastern = pytz.timezone("US/Eastern")
    last_updated = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p")
    
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
    
@app.route("/final_four")
def final_four():
    team_stats = teamStats(df, Top4)
    return render_template(
        "final_four.html",
        winner=Top4["winner"],
        runner_up=Top4["runner_up"],
        final_four=Top4["final_four"],
        team_stats=team_stats
    )

if __name__ == "__main__":
    app.run(debug=True)

