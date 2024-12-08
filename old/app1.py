from flask import Flask, jsonify, render_template, url_for
import os
import pandas as pd

app = Flask(__name__)

# Load teams data and group by predicted seed
def load_teams(file):
    df = pd.read_csv(file)
    df["TEAM1"] = df["TEAM"].str.replace("\xa0", "-")
    df["TEAM1"] = df["TEAM1"].str.split(r"-|vs").str[0]
    df.sort_values(by="predicted_seed_with_update", inplace=True)

    # Group teams by predicted_seed_with_update
    grouped_teams = df.groupby("predicted_seed_with_update")["TEAM1"].apply(list).to_dict()

    # Add image paths for each team
    for seed, teams in grouped_teams.items():
        grouped_teams[seed] = [
            {
                "name": team,
                "logo": find_team_logo(team)  # Find the logo dynamically
            }
            for team in teams
        ]

    return grouped_teams

def find_team_logo(team_name):
    # Static folder path for team logos
    logos_path = os.path.join(app.static_folder, "logos")
    # Generate the expected logo file path
    logo_file = f"{team_name}.png"
    logo_path = os.path.join(logos_path, logo_file)

    # Check if the logo exists, otherwise use a placeholder
    if os.path.exists(logo_path):
        return url_for('static', filename=f"logos/{logo_file}")
    else:
        return url_for('static', filename="logos/placeholder.png")  # Default logo

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_teams")
def get_teams():
    file_for_seed = "cbb25_seeded_20241122.csv"  # Update with your actual file path
    grouped_teams = load_teams(file_for_seed)
    return jsonify(grouped_teams)

@app.route("/final_four")
def final_four():
    # For now, you can mock the Final Four data. 
    # Later, you can calculate it dynamically based on the prediction model.
    final_four_teams = [
        {"name": "Team 1", "logo": url_for('static', filename="logos/team1.png")},
        {"name": "Team 2", "logo": url_for('static', filename="logos/team2.png")},
        {"name": "Team 3", "logo": url_for('static', filename="logos/team3.png")},
        {"name": "Team 4", "logo": url_for('static', filename="logos/team4.png")},
    ]
    
    return render_template("final_four.html", teams=final_four_teams)


if __name__ == "__main__":
    app.run(debug=True)
