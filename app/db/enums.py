import enum


class FileStatus(enum.Enum):
    valid = "valid"
    invalid = "invalid"


class FileType(enum.Enum):
    csv = "csv"
    text = "text"
