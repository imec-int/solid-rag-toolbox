from typing import Dict, List, Any
from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    question: str = Field(..., description="Question to be asked")
    user_data_requested: list = Field(...,
                                      description="List of user data requested")
    type: str = Field(..., description="Type of data requested")
    full_document: bool = Field(False, description="Return full document")


class ResponseBody(BaseModel):
    data: Dict[str, Any]
    errors: List[str]


class DocumentsRequestBody(BaseModel):
    documents: List[str] = Field(..., description="List of documents")
    inputType: str = Field(..., description="Type of input data")
    chunkType: str = Field(..., description="Type of chunking")
    metadata: Dict[str, Any] = Field({}, description="Metadata")
