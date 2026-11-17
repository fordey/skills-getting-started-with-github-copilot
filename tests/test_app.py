from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_rejects_student_already_registered():
    email = activities["Chess Club"]["participants"][0]
    participants_before = activities["Chess Club"]["participants"].copy()

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity"}
    assert activities["Chess Club"]["participants"] == participants_before


def test_delete_removes_student_from_activity():
    email = "temporary-student@mergington.edu"
    participants = activities["Chess Club"]["participants"]
    participants.append(email)

    try:
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": email},
        )

        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from Chess Club"}
        assert email not in participants
    finally:
        if email in participants:
            participants.remove(email)


def test_delete_rejects_student_not_signed_up():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "not-signed-up@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
