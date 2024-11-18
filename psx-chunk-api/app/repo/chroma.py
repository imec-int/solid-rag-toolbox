import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from app.config import load
import uuid

emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_chroma():
    config = load.Settings()
    client = chromadb.HttpClient(
        host=config.chromadb.host,
        port=config.chromadb.port,
        settings=Settings(allow_reset=False),
    )
    return client


def store_documents(documents: list, data_owner: str, metadata: dict = None):
    client = get_chroma()

    collection = client.get_or_create_collection(
        name="personal_collection", embedding_function=emb_fn
    )

    if documents is None or len(documents) == 0:
        return False

    if isinstance(documents[0], list):
        for doc in documents:
            store_chunked_document(collection, doc, data_owner, metadata)
    else:
        store_chunked_document(collection, documents, data_owner, metadata)

    return True


def store_chunked_document(collection, document, data_owner, metadata: dict = None):
    # Set a unique id for the document set
    document_set_id = str(uuid.uuid4())

    # Add the chunks as documents and link them to the
    # - document set
    # - index of the chunk in the document set
    # - owner
    metadatas = []
    for i in range(len(document)):
        doc_metadata = {
            "index": i,
            "document_set_id": document_set_id,
            "owner": data_owner,
        }
        for key, value in metadata.items():
            doc_metadata.update({key: value})

        metadatas.append(doc_metadata)

    collection.add(
        documents=document,
        # everything belongs to the same document, link all the chunked / splitted documents to the same document
        metadatas=metadatas,
        ids=[f"{uuid.uuid4()}" for _ in range(len(document))],
    )
