from pydantic import BaseModel
from enum import Enum


class ChunkType(str, Enum):
    OBJECT = "OBJECT"
    TOKENS = "TOKENS"
    SENTENCE = "SENTENCE"
    PARAGRAPH = "PARAGRAPH"


class InputType(str, Enum):
    JSON = "JSON"
    TEXT = "TEXT"


class DocumentsBody(BaseModel):
    chunkType: ChunkType
    inputType: InputType
    documents: list
    data_owner: str
    metadata: dict = None
