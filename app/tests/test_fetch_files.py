from datetime import datetime

from app.db.models import File, User


def test_fetch_files(authenticated_client, db_session):

    user = User(email="test1@gmail.com", password="password123")
    db_session.add(user)
    db_session.commit()

    assert db_session.query(User).count() == 2

    file = File(title="test_file", file_type="csv", valid_invalid="valid", user_id=user.id, size=100, upload_date=datetime(2021, 1, 1))  # noqa
    db_session.add(file)
    db_session.commit()

    response = authenticated_client.get(f"/files/users/{user.email}")

    assert response.status_code == 200

    assert response.json() == [{'id': 1, 'title': 'test_file', 'file_type': 'csv', 'size': 100, 'valid_invalid': 'valid', 'upload_date': '2021-01-01T00:00:00', 'csv_rows': 0}]  # noqa

    assert db_session.query(File).count() == 1
