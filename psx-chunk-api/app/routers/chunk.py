from app.repo.chroma import store_documents
from app.utils.chunking import chunkOnParagraphs, chunkOnSentences, chunkOnTokens
from app.utils.utils import jsonListToStringList, validateChunkType, validateInputType
from fastapi import APIRouter
from app.models.documents import ChunkType, DocumentsBody, InputType
from app.config import load

router = APIRouter()


@router.post(
    "/documents",
    name="Store documents",
    tags=[""],
    description="Store documents in the database",
)
def documents(docs: DocumentsBody):
    config = load.Settings()

    if not validateInputType(docs.inputType):
        return {"message": "Invalid inputType"}

    if not validateChunkType(docs.chunkType):
        return {"message": "Invalid chunkType"}

    match docs.inputType:
        case InputType.JSON:
            parsedDocs = jsonListToStringList(docs.documents)
        case InputType.TEXT:
            parsedDocs = docs.documents

    if len(parsedDocs) == 0:
        return {"message": "No documents to store"}

    chunks = []
    match docs.chunkType:
        case ChunkType.OBJECT:
            # chunk documents based on objects. No chunking required. (json = list of objects, text = list of strings)
            chunks = parsedDocs
            pass
        case ChunkType.TOKENS:
            # chunk documents based on tokens (# of characters)
            chunks = chunkOnTokens(parsedDocs, config.chunk_size_tokens)
            pass
        case ChunkType.SENTENCE:
            # chunk documents based on sentence (period)
            chunks = chunkOnSentences(parsedDocs)
            pass
        case ChunkType.PARAGRAPH:
            chunks = chunkOnParagraphs(parsedDocs)
            pass

    store_documents(
        documents=chunks, data_owner=docs.data_owner, metadata=docs.metadata
    )

    return {"message": f"Successfully stored {len(parsedDocs)} documents."}
