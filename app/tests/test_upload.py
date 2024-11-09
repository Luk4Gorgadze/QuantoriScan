import io

import pytest


@pytest.fixture
def txt_file():
    file_content = b"This is a test file."
    file = io.BytesIO(file_content)
    file.name = "testfile.txt"
    return file


@pytest.fixture
def csv_file():
    csv_content = "User,Company Name,Age\nJohn Doe,Quantori,32\nJanne Doe,Quantori,32\n"
    file = io.BytesIO(csv_content.encode("utf-8"))
    file.name = "testfile.csv"
    return file


def test_upload_txt(authenticated_client, txt_file):

    response = authenticated_client.post(
        "/upload",
        files={"file": (txt_file.name, txt_file, "text/plain")},
        data={"title": "testfile.txt", "file_type": "txt", "size": 100}
    )

    assert response.status_code == 202
    assert "task_id" in response.json()


def test_upload_csv(authenticated_client, csv_file):
    response = authenticated_client.post(
        "/upload",
        files={"file": (csv_file.name, csv_file, "text/csv")},
        data={"title": "testfile.csv", "file_type": "csv", "size": 200}
    )

    assert response.status_code == 202
    assert "task_id" in response.json()
