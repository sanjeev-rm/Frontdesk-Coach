"""
RAG System Module (YAML-backed)

Provides the retriever implementation used by coaching and reporting agents.
The project uses a YAML-backed retriever by default when a single knowledge
file (`hotel_training_reference.yaml`) is the canonical source.
"""

from .retriever import RAGRetriever

__all__ = ['RAGRetriever']