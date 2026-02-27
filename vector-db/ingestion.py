"""Ingestion ChromaDB vector store with similarity threshold filtering."""

import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    def __init__(self, collection_name="dark_psychology"):
        self.client = chromadb.Client()
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=self.ef
        )

    def add_documents(self, docs):
        self.collection.add(
            documents=[d["text"] for d in docs],
            metadatas=[d["metadata"] for d in docs],
            ids=[f"doc_{i}" for i in range(len(docs))],
        )
        print(f"Successfully ingested {len(docs)} document chunks.")

    @staticmethod
    def _distance_to_similarity(distance):
        return 1 / (1 + distance)

    def query_with_threshold(self, user_query, n_results=5, threshold=0.8):
        """Retrieve chunks, silently filter by threshold.
        Returns context (empty if nothing passes) for the LLM."""
        results = self.collection.query(
            query_texts=[user_query],
            n_results=n_results,
            include=["documents", "distances", "metadatas"],
        )
        docs = results["documents"][0]
        dists = results["distances"][0]
        metas = results["metadatas"][0]

        scored = sorted(
            [(d, round(self._distance_to_similarity(dist), 4), m)
             for d, dist, m in zip(docs, dists, metas)],
            key=lambda x: x[1], reverse=True
        )
        passed = [s for s in scored if s[1] >= threshold]

        return {
            "context": "\n\n".join(t for t, _, _ in passed) if passed else "",
            "sources": passed,
            "is_relevant": len(passed) > 0,
        }