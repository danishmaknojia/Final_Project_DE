import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_final_four_route(client):
    """Test the Final Four route."""
    response = client.get("/final_four")
    assert response.status_code == 200
    assert b"Final Four" in response.data

def test_health_route(client):
    """Test the health check route."""
    response = client.get("/health")
    assert response.status_code == 200
    assert b"Healthy" in response.data


# Run All Tests
def run_all_tests():
    test_final_four_route()
    test_health_route()
    print("All tests passed!")


if __name__ == "__main__":
    run_all_tests()
