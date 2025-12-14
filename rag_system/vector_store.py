"""
Deprecated Vector Store Module

This project no longer uses a ChromaDB-based vector store by default. The YAML-backed
retriever in `rag_system.retriever` provides the canonical retrieval mechanism when
the knowledge base is a single YAML file. This module remains as a placeholder; importing
it will raise an informative error.
"""

raise ImportError(
    "VectorStore has been removed. The project now uses a YAML-backed retriever."
)