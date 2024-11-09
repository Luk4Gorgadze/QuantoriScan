import csv
import io
from typing import Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import File
from app.db.schemas import FileStatus, FileType


def handle_csv(file_contents: bytes, db: Session, file_name: str, file_size: int, user_id: int) -> bool:
    try:
        csv_data = io.StringIO(file_contents.decode("utf-8"))
        csv_reader = csv.reader(csv_data)

        headers = get_headers(csv_reader)
        if not headers:
            return False

        company_name_index = get_company_name_index(headers)
        if company_name_index is None:
            return False

        target_word = "Quantori"
        valid_file, row_count = process_csv_rows(csv_reader, company_name_index, target_word)

        if valid_file:
            save_file_to_db(db, file_name, file_size, user_id, row_count, FileType.csv)
            return True
        else:
            return False

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV file: {str(e)}")


def get_headers(csv_reader) -> list:
    return next(csv_reader, None)


def get_company_name_index(headers: list) -> int:
    try:
        return headers.index("Company Name")
    except ValueError:
        return None


def process_csv_rows(csv_reader, company_name_index: int, target_word: str) -> Tuple[bool, int]:
    valid_file = False
    row_count = 0

    for row in csv_reader:
        row_count += 1
        if len(row) <= company_name_index:
            continue

        if row[company_name_index] == target_word:
            valid_file = True

        if target_word in [col for i, col in enumerate(row) if i != company_name_index]:
            return False, row_count

    return valid_file, row_count


def save_file_to_db(db: Session, file_name: str, file_size: int, user_id: int, row_count: int, file_type: FileType):
    new_file = File(
        title=file_name,
        file_type=file_type,
        valid_invalid=FileStatus.valid,
        user_id=user_id,
        size=file_size,
        csv_rows=row_count if file_type == FileType.csv else None,
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)


def handle_text(file_contents: bytes, db: Session, file_name: str, file_size: int, user_id: int) -> bool:
    try:
        text_content = file_contents.decode("utf-8")
        contains_quantori = "Quantori" in text_content

        if contains_quantori:
            save_file_to_db(db, file_name, file_size, user_id, None, FileType.text)
            return True
        else:
            return False

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing text file: {str(e)}")
