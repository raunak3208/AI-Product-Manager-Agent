import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection(name="pm_agent_memory")

def save_memory(doc_id: str, text: str, metadata: dict = None) -> None:
    collection.add(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata or {}],
    )

def retrieve_memory(query: str, n_results: int = 3) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )
    return results["documents"][0]