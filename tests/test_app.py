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
