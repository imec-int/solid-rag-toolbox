from pydantic import BaseModel
from enum import StrEnum, auto


class DocType(StrEnum):
    CALENDAR = auto()
    NOTES = auto()
    FINANCIAL = auto()
    EMAILS = auto()
    MEDICAL = auto()


class SearchQuery(BaseModel):
    question: str
    user_data_requested: list[str]
    type: DocType
    full_document: bool
