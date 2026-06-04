import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_activity_succeeds(self, client_with_fresh_activities):
        """Test that a valid signup succeeds and returns success message.

        AAA Pattern:
        - Arrange: Prepare activity name and email
        - Act: Send POST request to signup endpoint
        - Assert: Status 200 and message confirms signup
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Chess Club"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client_with_fresh_activities):
        """Test that signup actually adds the participant to the activity.

        AAA Pattern:
        - Arrange: Prepare activity name and email
        - Act: Sign up student, then fetch activities
        - Assert: Participant appears in activity's participant list
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        fetch_response = client.get("/activities")
        activities = fetch_response.json()

        # Assert
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client_with_fresh_activities):
        """Test that signup for non-existent activity returns 404.

        AAA Pattern:
        - Arrange: Prepare non-existent activity name
        - Act: Send POST request
        - Assert: Status 404 and error detail provided
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_email_returns_400(self, client_with_fresh_activities):
        """Test that duplicate signup for same activity returns 400.

        AAA Pattern:
        - Arrange: Sign up once with an email
        - Act: Attempt to sign up with same email again
        - Assert: Status 400 and error indicates duplicate
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already signed up

        # Act
        first_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        second_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert first_response.status_code == 400
        assert second_response.status_code == 400
        data = second_response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_with_special_characters_in_email(self, client_with_fresh_activities):
        """Test that signup works with email containing special characters.

        AAA Pattern:
        - Arrange: Prepare email with special characters
        - Act: Send signup request with encoded email
        - Assert: Status 200 and participant added
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Drama Society"
        email = "user+tag@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
