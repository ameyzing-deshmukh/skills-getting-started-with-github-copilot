import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provides a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets the activities database to a known state.
    Yields the activities dict, then restores original state after test.
    """
    # Store original state
    original_activities = {key: {
        "description": val["description"],
        "schedule": val["schedule"],
        "max_participants": val["max_participants"],
        "participants": val["participants"].copy()
    } for key, val in activities.items()}

    # Clear and rebuild for test
    activities.clear()
    activities.update(original_activities)

    yield activities

    # Restore original state
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client_with_fresh_activities(client, reset_activities):
    """Combines TestClient and reset activities for convenience."""
    return client
