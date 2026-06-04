import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_all_activities_returns_dict(self, client_with_fresh_activities):
        """Test that GET /activities returns all activities.

        AAA Pattern:
        - Arrange: TestClient is ready
        - Act: Make GET request to /activities
        - Assert: Status 200 and response is a non-empty dict
        """
        # Arrange
        client = client_with_fresh_activities

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_activity_has_required_fields(self, client_with_fresh_activities):
        """Test that each activity contains all required fields.

        AAA Pattern:
        - Arrange: TestClient is ready
        - Act: Make GET request and extract first activity
        - Assert: Verify required fields exist and have correct types
        """
        # Arrange
        client = client_with_fresh_activities
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = list(activities.values())[0]

        # Assert
        assert all(field in first_activity for field in required_fields)
        assert isinstance(first_activity["description"], str)
        assert isinstance(first_activity["schedule"], str)
        assert isinstance(first_activity["max_participants"], int)
        assert isinstance(first_activity["participants"], list)

    def test_participants_is_list_of_strings(self, client_with_fresh_activities):
        """Test that participants field contains email strings.

        AAA Pattern:
        - Arrange: TestClient is ready
        - Act: Make GET request and check participants
        - Assert: Each participant is a non-empty string
        """
        # Arrange
        client = client_with_fresh_activities

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert len(participant) > 0
