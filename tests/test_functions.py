import pandas as pd
import os
from functions import (
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
    team_logo = findTeamLogo("Team A")
    assert "Team A" in team_logo or "placeholder.png" in team_logo
    print("test_findTeamLogo passed!")


def test_findConferenceLogo():
    conference_logo = findConferenceLogo("Conf1")
    assert "Conf1" in conference_logo or "placeholder.png" in conference_logo
    print("test_findConferenceLogo passed!")


def test_loadTeams():
    teams = loadTeams(mock_data)
    assert "TEAM1" in teams.columns
    assert len(teams) == 4  # Mock data has 4 rows
    print("test_loadTeams passed!")


def test_extractSeeds():
    teams = loadTeams(mock_data)
    seeds = extractSeeds(teams)
    assert 1 in seeds
    assert len(seeds[1]) > 0  # Teams with seed 1 should exist
    print("test_extractSeeds passed!")


def test_extractFirstLastRanks():
    teams = loadTeams(mock_data)
    rank1, rank67, rank68 = extractFirstLastRanks(teams)
    assert rank1["rank"] == 1
    assert rank67["rank"] == 67
    assert rank68["rank"] == 68
    print("test_extractFirstLastRanks passed!")


def test_extractConferences():
    teams = loadTeams(mock_data)
    conferences = extractConferences(teams)
    assert "Conf1" in conferences
    assert len(conferences["Conf1"]["teams"]) > 0  # Teams in Conf1 should exist
    print("test_extractConferences passed!")


def test_finalFour():
    top_four = finalFour(mock_data)
    assert len(top_four["final_four"]) == 4  # Should predict 4 teams
    assert "winner" in top_four
    assert "runner_up" in top_four
    print("test_finalFour passed!")


def test_teamStats():
    top_four = finalFour(mock_data)
    stats = teamStats(mock_data, top_four)
    assert len(stats) == 4  # Should have stats for 4 teams
    assert "Team" in stats[0]  # Check if team stats have the correct structure
    print("test_teamStats passed!")


# Run All Tests
def run_all_tests():
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
