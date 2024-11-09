from datetime import datetime

import pytest
from fastapi import status

from app.db.models import Comment, File, User


@pytest.fixture
def file_with_user(db_session):
    user = User(email="test1@gmail.com", password="password123")
    db_session.add(user)
    db_session.commit()

    file = File(title="test_file", file_type="csv", valid_invalid="valid", user_id=user.id, size=100, upload_date=datetime(2021, 1, 1))  # noqa
    db_session.add(file)
    db_session.commit()
    return file


@pytest.fixture
def file_with_comments(file_with_user, db_session):
    file_with_user.comments = [
        Comment(text="test comment 1", user_id=file_with_user.user_id, file_id=file_with_user.id),
        Comment(text="test comment 2", user_id=file_with_user.user_id, file_id=file_with_user.id),
    ]

    db_session.commit()
    return file_with_user


def test_add_comment(authenticated_client, db_session, file_with_user):

    response = authenticated_client.post(f"/comments/files/{file_with_user.id}", json={"text": "test comment"})

    assert response.status_code == status.HTTP_201_CREATED


def test_get_comments_for_file(authenticated_client, db_session, file_with_comments):

    response = authenticated_client.get(f"/comments/files/{file_with_comments.id}")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 2
