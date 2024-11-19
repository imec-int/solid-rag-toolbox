import logging
import numpy as np
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from chromadb.api.types import QueryResult
from sentence_transformers import CrossEncoder

from app.models.search import SearchQuery
from app.config import load

COLLECTION = "personal_collection"

emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_chroma():
    config = load.Settings()
    client = chromadb.HttpClient(
        host=config.chromadb.host,
        port=config.chromadb.port,
        settings=Settings(allow_reset=True),
    )
    return client


def search_embeddings(query: SearchQuery):
    logging.info("Searching ChromaDB")
    vector_store = get_chroma()

    collection = vector_store.get_or_create_collection(
        name=COLLECTION, embedding_function=emb_fn
    )

    if len(query.user_data_requested) > 1:
        ownersQuery = {"$or": [{"owner": owner}
                               for owner in query.user_data_requested]}
    else:
        ownersQuery = {"owner": query.user_data_requested[0]}

    whereClause = {"$and": [ownersQuery, {"type": query.type.value}]}

    # Initial query to find relevant chunks
    initial_results = collection.query(
        query_texts=[query.question], n_results=5, where=whereClause
    )

    combined_results: QueryResult = {
        "ids": [[]],
        "distances": [[]],
        "embeddings": None,
        "documents": [[]],
        "metadatas": [[]],
        "uris": None,
        "data": None,
        "included": [],
        "highestScore": None,
    }

    if query.full_document:
        # Get all document_set_ids from the initial results
        if len(initial_results["documents"][0]) > 0:
            logging.info("Getting all documents from document set")
            document_set_ids = set()
            for metadata in initial_results["metadatas"][0]:
                document_set_ids.add(metadata["document_set_id"])

            # Get all documents based on the document_set_ids
            results = []
            for document_set_id in document_set_ids:
                whereClause = {
                    "$and": [
                        ownersQuery,
                        {"type": query.type.value},
                        {"document_set_id": document_set_id},
                    ]
                }
                document_set_results = collection.query(
                    # Empty query to retrieve all relevant chunks
                    query_texts=[""],
                    # Assuming there won't be more than 1000 chunks per document set
                    n_results=1000,
                    where=whereClause,
                )
                results.append(document_set_results)

            # Combine all results
            for item in results:
                combined_results["ids"][0].extend(item["ids"][0])
                combined_results["distances"][0].extend(item["distances"][0])
                combined_results["metadatas"][0].extend(item["metadatas"][0])
                combined_results["documents"][0].extend(item["documents"][0])
    else:
        logging.info("Getting chunks from query")
        combined_results = initial_results

    if len(combined_results["documents"][0]) == 0:
        return combined_results
    
    # Check for highest scoring document
    model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2", max_length=512)
    # rerank the results with original query and documents returned from Chroma
    scores = model.predict([(query.question, doc)
                            for doc in combined_results["documents"][0]])
    # get the highest scoring document
    combined_results["highestScore"] = combined_results["documents"][0][np.argmax(
        scores)]

    return combined_results
