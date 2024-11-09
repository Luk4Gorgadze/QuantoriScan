import io
from unittest.mock import patch

import pytest

from app.db.models import File
from app.logic.file_handlers import handle_csv, handle_text


@pytest.fixture
def txt_file_invalid():
    file_content = "Some invalid text".encode("utf-8")
    file = io.BytesIO(file_content)
    file.name = "testfile.txt"
    return file


@pytest.fixture
def txt_file_valid():
    file_content = "Some Quantori valid text".encode("utf-8")
    file = io.BytesIO(file_content)
    file.name = "testfile.txt"
    return file


@pytest.fixture
def csv_file_valid():
    csv_content = "User,Company Name,Age\nJohn Doe,Quantori,32\nJanne Doe,Quantori,32\n"
    file = io.BytesIO(csv_content.encode("utf-8"))
    file.name = "testfile.csv"
    return file


@pytest.fixture
def csv_file_invalid():
    csv_content = "User,Company Name,Age\nJohn Doe,Quantori,32\nQuantori,RandomCompany,33\n"
    file = io.BytesIO(csv_content.encode("utf-8"))
    file.name = "testfile.csv"
    return file


def test_handle_txt_invalid(client, db_session, txt_file_invalid):
    with patch('app.logic.file_handlers.save_file_to_db') as mock_save:
        mock_save.return_value = None

        file_contents = txt_file_invalid.read()

        handle_text(file_contents, db_session, "testfile.txt", 100, 1)

        assert db_session.query(File).count() == 0


def test_handle_txt_valid(client, db_session, txt_file_valid):
    with patch('app.logic.file_handlers.save_file_to_db') as mock_save:
        mock_save.return_value = None

        file_contents = txt_file_valid.read()

        handle_text(file_contents, db_session, "testfile.txt", 100, 1)

        mock_save.assert_called_once()


def test_handle_csv_invalid(client, db_session, csv_file_invalid):
    with patch('app.logic.file_handlers.save_file_to_db') as mock_save:
        mock_save.return_value = None

        file_contents = csv_file_invalid.read()

        handle_csv(file_contents, db_session, "testfile.csv", 100, 1)

        assert db_session.query(File).count() == 0


def test_handle_csv_valid(client, db_session, csv_file_valid):
    with patch('app.logic.file_handlers.save_file_to_db') as mock_save:
        mock_save.return_value = None

        file_contents = csv_file_valid.read()

        handle_csv(file_contents, db_session, "testfile.csv", 100, 1)

        mock_save.assert_called_once()
