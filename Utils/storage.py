import chromadb
from chromadb.config import Settings


client = chromadb.PersistentClient(
    settings=Settings(
        persist_directory="./data/chroma_storage"
    )
)


collection = client.get_or_create_collection("document_collection")

def add_document(document_id: str, text: str, embedding):
    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"id": document_id}]
    )

def query_documents(query_embedding, top_k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
