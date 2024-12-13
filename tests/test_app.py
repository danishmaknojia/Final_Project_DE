import pytest
from app import app

# Pytest fixture for the Flask test client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_final_four_route(client):
    """
    Test the Final Four route.
    """
    response = client.get("/final_four")
    # Response status code
    assert response.status_code == 200  # Route exists and works
    # Expected content in the response
    assert b"Final Four" in response.data


def test_health_route(client):
    """
    Test the health check route.
    """
    response = client.get("/health")
    assert response.status_code == 200  # Should return OK
    assert b"Healthy" in response.data  # Verify health status text


def test_nonexistent_route(client):
    """
    Test a nonexistent route to ensure the app handles 404 errors properly.
    """
    response = client.get("/nonexistent")
    assert response.status_code == 404  # Should return a 404 for nonexistent routes


# Run All Tests
def run_all_tests():
    test_index_route()
    test_final_four_route()
    test_health_route()
    test_nonexistent_route()
    print("All tests passed!")


if __name__ == "__main__":
    run_all_tests()
