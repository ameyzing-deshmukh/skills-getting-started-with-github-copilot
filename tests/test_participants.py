import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_succeeds(self, client_with_fresh_activities):
        """Test that removing an existing participant succeeds.

        AAA Pattern:
        - Arrange: Identify an existing participant
        - Act: Send DELETE request to remove participant
        - Assert: Status 200 and message confirms removal
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_actually_removes_from_list(self, client_with_fresh_activities):
        """Test that removal actually removes participant from activity.

        AAA Pattern:
        - Arrange: Fetch initial participant count
        - Act: Remove a participant
        - Assert: Participant no longer in list and count decreased
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Basketball Team"
        email = "nina@mergington.edu"

        # Get initial participant list
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        delete_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Fetch updated list
        final_response = client.get("/activities")
        final_activities = final_response.json()
        final_count = len(final_activities[activity_name]["participants"])

        # Assert
        assert delete_response.status_code == 200
        assert email not in final_activities[activity_name]["participants"]
        assert final_count == initial_count - 1

    def test_remove_participant_from_nonexistent_activity_returns_404(self, client_with_fresh_activities):
        """Test that removing from non-existent activity returns 404.

        AAA Pattern:
        - Arrange: Prepare non-existent activity name
        - Act: Send DELETE request
        - Assert: Status 404 with error detail
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_nonexistent_participant_returns_404(self, client_with_fresh_activities):
        """Test that removing non-existent participant returns 404.

        AAA Pattern:
        - Arrange: Prepare email not in activity
        - Act: Send DELETE request
        - Assert: Status 404 with error detail
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Swimming Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_participant_leaves_others_unchanged(self, client_with_fresh_activities):
        """Test that removing one participant doesn't affect others.

        AAA Pattern:
        - Arrange: Get list of participants
        - Act: Remove one participant
        - Assert: Other participants still in list
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Art Club"

        # Get initial participants
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        initial_participants = initial_activities[activity_name]["participants"].copy()
        email_to_remove = initial_participants[0]
        other_emails = initial_participants[1:]

        # Act
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )

        # Fetch updated list
        final_response = client.get("/activities")
        final_activities = final_response.json()
        final_participants = final_activities[activity_name]["participants"]

        # Assert
        for other_email in other_emails:
            assert other_email in final_participants

    def test_remove_participant_with_special_email_characters(self, client_with_fresh_activities):
        """Test that removal works with special characters in email.

        AAA Pattern:
        - Arrange: Add participant with special email, then attempt removal
        - Act: Send DELETE with encoded special email
        - Assert: Status 200 and participant removed
        """
        # Arrange
        client = client_with_fresh_activities
        activity_name = "Math Olympiad"
        email = "user+special@mergington.edu"

        # First, add the participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Verify removal
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
