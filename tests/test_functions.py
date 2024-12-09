import pandas as pd
import os
from mylib.functions import (
    findTeamLogo,
    findConferenceLogo,
    loadTeams,
    extractSeeds,
    extractFirstLastRanks,
    extractConferences,
    finalFour,
    teamStats,
)

# Mock DataFrame simulating the structure of the CSV
mock_data = pd.DataFrame({
    "TEAM": ["Team A", "Team B", "Team C", "Team D"],
    "CONF": ["Conf1", "Conf2", "Conf1", "Conf3"],
    "predicted_seed_with_update": [1, 2, 1, 3],
    "rank": [1, 68, 2, 67],
    "predicted_seed_score": [95.0, 85.0, 90.0, 80.0],
    "predicted_postseason_label": [1, 4, 2, 3],
    "predicted_postseason_description": ["Winner", "Final Four", "Runner Up", "Final Four"],
    "G": [30, 28, 32, 29],
    "ADJOE": [115.0, 105.0, 110.0, 102.0],
    "ADJDE": [95.0, 98.0, 97.0, 100.0],
    "BARTHAG": [0.85, 0.65, 0.75, 0.60],
    "EFG_O": [55.0, 50.0, 53.0, 48.0],
    "EFG_D": [48.0, 52.0, 49.0, 53.0],
    "TOR": [15.0, 18.0, 16.0, 19.0],
    "TORD": [10.0, 12.0, 11.0, 13.0],
    "ORB": [32.0, 30.0, 31.0, 29.0],
    "DRB": [68.0, 70.0, 69.0, 71.0],
    "FTR": [30.0, 25.0, 28.0, 24.0],
    "FTRD": [20.0, 22.0, 21.0, 23.0],
})

# Test Functions
def test_findTeamLogo():
    """Test if team logos are correctly found or default placeholder is used."""
    logo = findTeamLogo("Team A")
    assert "Team A" in logo or "placeholder.png" in logo, "Team A logo not found as expected."
    print("test_findTeamLogo passed!")

def test_findConferenceLogo():
    """Test if conference logos are correctly found or default placeholder is used."""
    logo = findConferenceLogo("Conf1")
    assert "Conf1" in logo or "placeholder.png" in logo, "Conference logo not found as expected."
    print("test_findConferenceLogo passed!")

def test_loadTeams():
    """Test if teams are loaded and cleaned correctly."""
    teams = loadTeams(mock_data)
    assert "TEAM1" in teams.columns, "'TEAM1' column missing in processed data."
    assert len(teams) == len(mock_data), "Mismatch in number of rows after processing."
    print("test_loadTeams passed!")

def test_extractSeeds():
    """Test if teams are grouped correctly by seeds."""
    teams = loadTeams(mock_data)
    seeds = extractSeeds(teams)
    assert 1 in seeds, "Seed 1 is missing in grouped data."
    assert len(seeds[1]) > 0, "No teams found for Seed 1."
    print("test_extractSeeds passed!")

def test_extractFirstLastRanks():
    """Test if the first, second-to-last, and last-ranked teams are extracted correctly."""
    teams = loadTeams(mock_data)
    rank1, rank67, rank68 = extractFirstLastRanks(teams)
    assert rank1["rank"] == 1, "Rank 1 team is incorrect."
    assert rank67["rank"] == 67, "Second-to-last team rank is incorrect."
    assert rank68["rank"] == 68, "Last-ranked team is incorrect."
    print("test_extractFirstLastRanks passed!")

def test_extractConferences():
    """Test if teams are grouped correctly by conference with logos added."""
    teams = loadTeams(mock_data)
    conferences = extractConferences(teams)
    assert "Conf1" in conferences, "Conf1 is missing in grouped conference data."
    assert len(conferences["Conf1"]["teams"]) > 0, "No teams found for Conf1."
    print("test_extractConferences passed!")

def test_finalFour():
    """Test if the top 4 teams are correctly predicted for the Final Four."""
    top_four = finalFour(mock_data)
    assert len(top_four["final_four"]) == 4, "Final Four prediction did not return 4 teams."
    assert "winner" in top_four, "Winner not identified in Final Four prediction."
    assert "runner_up" in top_four, "Runner-up not identified in Final Four prediction."
    print("test_finalFour passed!")

def test_teamStats():
    """Test if the team statistics for the Final Four are correctly extracted."""
    top_four = finalFour(mock_data)
    stats = teamStats(mock_data, top_four)
    assert len(stats) == 4, "Team statistics not generated for all 4 Final Four teams."
    assert "Team" in stats[0], "Team name missing in statistics."
    assert "Conference" in stats[0], "Conference name missing in statistics."
    print("test_teamStats passed!")

# Run All Tests
def run_all_tests():
    """Run all test cases."""
    test_findTeamLogo()
    test_findConferenceLogo()
    test_loadTeams()
    test_extractSeeds()
    test_extractFirstLastRanks()
    test_extractConferences()
    test_finalFour()
    test_teamStats()
    print("All tests passed!")

if __name__ == "__main__":
    run_all_tests()
