from fastapi import APIRouter
from app.models.search import SearchQuery
from app.repo.chroma import search_embeddings

router = APIRouter()


@router.post("/invoke", tags=["vector search"], description="Vector search embeddings")
def search(query: SearchQuery):
    documents = search_embeddings(query)
    return {
        "documents": documents,
        "user_data_requested": query.user_data_requested,
        "question": query.question,
    }
