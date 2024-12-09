# import pytest
# from app import app

# @pytest.fixture
# def client():
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client

# def test_final_four_route(client):
#     """Test the Final Four route."""
#     response = client.get("/final_four")
#     assert response.status_code == 200
#     assert b"Final Four" in response.data

# def test_health_route(client):
#     """Test the health check route."""
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert b"Healthy" in response.data


# # Run All Tests
# def run_all_tests():
#     test_final_four_route()
#     test_health_route()
#     print("All tests passed!")


# if __name__ == "__main__":
#     run_all_tests()

import pytest
from app import app
from unittest.mock import patch

# Pytest fixture for the Flask test client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Mock S3 CSV loading function
@patch("app.read_s3_csv")
@patch("app.loadTeams")
@patch("app.finalFour")
def test_final_four_route(mock_finalFour, mock_loadTeams, mock_read_s3_csv, client):
    """
    Test the Final Four route.
    Mock dependencies for reading S3 data and data processing.
    """
    # Set up mock return values
    mock_read_s3_csv.return_value = "mock_dataframe"
    mock_loadTeams.return_value = "mock_cleaned_dataframe"
    mock_finalFour.return_value = {
        "final_four": ["Team A", "Team B", "Team C", "Team D"],
        "winner": "Team A",
        "runner_up": "Team B"
    }

    # Call the route
    response = client.get("/final_four")

    # Assertions
    assert response.status_code == 200
    assert b"Team A" in response.data  # Check if winner's name is in the response
    assert b"Final Four" in response.data


def test_health_route(client):
    """
    Test the health check route.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert b"Healthy" in response.data


if __name__ == "__main__":
    pytest.main(["-v"])
