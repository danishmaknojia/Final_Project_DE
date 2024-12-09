import os

def findTeamLogo(teamName):
    """
    Finds the team logo file path dynamically. Uses a placeholder if the logo doesn't exist.
    """
    # Static folder path for team logos
    logos_path = os.path.join("static", "logos")
    logo_file = f"{teamName}.png"
    logo_path = os.path.join(logos_path, logo_file)

    # Check if the logo exists, otherwise use a placeholder
    if os.path.exists(logo_path):
        return os.path.join("static", "logos", logo_file)
    else:
        return os.path.join("static", "logos", "placeholder.png")  # Default logo

def findConferenceLogo(conferenceName):
    """
    Finds the conference logo file path dynamically. Uses a placeholder if the logo doesn't exist.
    """
    # Static folder path for conference logos
    logos_path = os.path.join("static", "conferenceLogos")
    logo_file = f"{conferenceName}.png"
    logo_path = os.path.join(logos_path, logo_file)

    # Check if the logo exists, otherwise use a placeholder
    if os.path.exists(logo_path):
        return os.path.join("static", "conferenceLogos", logo_file)
    else:
        return os.path.join("static", "conferenceLogos", "placeholder.png")  # Default logo

def loadTeams(df):
    """
    Processes the DataFrame,
    extracting only required columns
    """ 
    # Clean team names
    df["TEAM1"] = df["TEAM"].str.replace("\xa0", "-")
    df["TEAM1"] = df["TEAM1"].str.split(r"-|vs").str[0]
    df.sort_values(by=["predicted_seed_with_update", "rank"], axis=0, inplace=True)
    
    # Extracting relevant columns
    dfClean = df[["TEAM1", "CONF", "predicted_seed_score", "rank", "predicted_seed_with_update", "predicted_postseason_label", "predicted_postseason_description"]]
    return dfClean

def extractSeeds(data):
    """
    Groups the teams by predicted seed, 
    adding logo paths for each team.
    """
    # Group teams by predicted seed
    df = data.groupby("predicted_seed_with_update")["TEAM1"].apply(list).to_dict()

    # Add image paths for each team
    for seed, teams in df.items():
        df[seed] = [{"name": team, "logo": findTeamLogo(team)} for team in teams]
        
    return df

def extractFirstLastRanks(df): 
    """
    Extracts the first, second-to-last, and last ranked teams
    and adds their logo paths.
    """
    # Sort by rank and reset index for consistent indexing
    df = df.sort_values(by="rank")
    df.reset_index(drop=True, inplace=True)

    # Extract the relevant rows
    Rank1 = df.iloc[0]
    Rank67 = df.iloc[-2]
    Rank68 = df.iloc[-1]

    # Add logo paths to each team's data
    Rank1 = {"TEAM1": Rank1["TEAM1"], "rank": Rank1["rank"], "logo": findTeamLogo(Rank1["TEAM1"])}
    Rank67 = {"TEAM1": Rank67["TEAM1"], "rank": Rank67["rank"], "logo": findTeamLogo(Rank67["TEAM1"])}
    Rank68 = {"TEAM1": Rank68["TEAM1"], "rank": Rank68["rank"], "logo": findTeamLogo(Rank68["TEAM1"])}

    return Rank1, Rank67, Rank68

def extractConferences(data):
    """
    Groups the teams by conference, adds logo paths for both teams and conferences, 
    and sorts conferences by team count in descending order.
    """
    # Group teams by conference
    grouped = data.groupby("CONF")["TEAM1"].apply(list).to_dict()
    
    # Add logos for each conference and their respective teams
    conference_data = {}
    for conf, teams in grouped.items():
        conference_data[conf] = {"logo": findConferenceLogo(conf),  # Add conference logo
                                 "teams": [{"name": team, "logo": findTeamLogo(team)} for team in teams]}  # Add team logos

    # Sort by the number of teams in descending order
    sortedConfCounts = dict(sorted(conference_data.items(), key=lambda item: len(item[1]["teams"]), reverse=True))

    return sortedConfCounts

## PAGE 2
def finalFour(data):
    """
    Extracts the predicted final four teams
    """
    sortByPredictedWinner = data.sort_values(by='predicted_postseason_label', ascending=True)
    topFour = sortByPredictedWinner.head(4)

    topFourDict = { "final_four": topFour["TEAM1"].tolist(), 
                   "runner_up": topFour["TEAM1"].iloc[1], 
                   "winner": topFour["TEAM1"].iloc[0] }
        
    return topFourDict  # This should return a dictionary
    
def teamStats(dataframe, topFour):
    top4teams = list(topFour['final_four'])  # Access the dictionary key 'final_four' correctly.
            
    # Filter the dataframe for rows with these team names in the 'TEAM1' column
    teamList = dataframe[dataframe['TEAM1'].isin(top4teams)]
    teamColumns = ["TEAM1", "CONF", 
                   "G", 
                   "ADJOE", "ADJDE", 
                   "BARTHAG", 
                   "EFG_O", "EFG_D", 
                   "TOR", "TORD", 
                   "ORB", "DRB", 
                   "FTR", "FTRD"]
    
    cleanedTeams = teamList[teamColumns]
    
    # Define the mapping
    column_mapping = {
        "TEAM1": "Team",
        "CONF": "Conference",
        "G": "Number of Games Played",
        "ADJOE": "Adjusted Offensive Efficiency",
        # ADJOE: (An estimate of the offensive efficiency a team would have against the average Division I defense)
        "ADJDE": "Adjusted Defensive Efficiency",
        # ADJDE:  (An estimate of the defensive efficiency a team would have against the average Division I offense)
        "BARTHAG": "Power Rating (Chance of beating an average Division I team)",
        "EFG_O": "Effective Field Goal Percentage Shot",
        "EFG_D": "Effective Field Goal Percentage Allowed",
        "TOR": "Turnover Rate",
        "TORD": "Steal Rate",
        "ORB": "Offensive Rebound Rate",
        "DRB": "Offensive Rebound Rate Allowed",
        "FTR": "Free Throw Rate", # (How often the given team shoots Free Throws)
        "FTRD": "Free Throw Rate Allowed"
    }
    
    # Rename the columns
    renamedColumnTeams = cleanedTeams.rename(columns=column_mapping, inplace=False)
    teamsDict = renamedColumnTeams.to_dict(orient="records")
    
    return teamsDict


# TESTING
# from lib import read_s3_csv
# import boto3
# from datetime import datetime
# s3 = boto3.client("s3")
# bucket_name = "cbb-data-engg"
# output_prefix = "Final_Project_DE/"
# current_date = datetime.now().strftime("%Y%m%d")
# file_name_final = f"cbb25_seeded_{current_date}.csv"
# data = read_s3_csv(bucket_name, f"{output_prefix}{file_name_final}")
# teams = loadTeams(data)
# dictionatyitem = finalFour(teams)
# stats = teamStats(data, dictionatyitem)
