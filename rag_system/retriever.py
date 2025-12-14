"""
YAML-backed Retriever

This retriever loads a single YAML reference file (`hotel_training_reference.yaml`) and
provides simple keyword-based retrieval over the document sections. The original RAG
vector/embedding approach is intentionally not used when a single YAML knowledge file
is the canonical source of truth.
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml

from config.settings import AppConfig


class RAGRetriever:
    """Simple retriever that uses the YAML reference as the knowledge base."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Path to the YAML reference file (default to repo root)
        self.yaml_path = Path("hotel_training_reference.yaml")
        if hasattr(self.config, 'BASE_DIR') and self.config.BASE_DIR:
            # Allow yaml in base dir
            possible = self.config.BASE_DIR / self.yaml_path.name
            if possible.exists():
                self.yaml_path = possible

        # In-memory list of documents (flattened YAML sections)
        self.documents: List[Dict[str, Any]] = []
        self._load_yaml()

    def _load_yaml(self) -> None:
        """Load and flatten the YAML file into searchable documents."""
        try:
            if not self.yaml_path.exists():
                self.logger.warning(f"YAML reference not found at {self.yaml_path}")
                self.documents = []
                return

            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Flatten nested dicts into title/content pairs
            flat_docs: List[Dict[str, Any]] = []

            def recurse(node, path_parts: List[str]):
                if isinstance(node, dict):
                    for k, v in node.items():
                        recurse(v, path_parts + [str(k)])
                elif isinstance(node, list):
                    # Join list items into text
                    content = "\n".join(str(item) for item in node)
                    title = " / ".join(path_parts)
                    flat_docs.append({"title": title, "content": content})
                else:
                    # Scalar value
                    title = " / ".join(path_parts)
                    flat_docs.append({"title": title, "content": str(node)})

            # YAML top-level may be a mapping
            if isinstance(data, dict):
                for top_k, top_v in data.items():
                    recurse(top_v, [str(top_k)])
            else:
                recurse(data, ["root"])

            # Assign ids and metadata
            for i, doc in enumerate(flat_docs):
                self.documents.append({
                    "id": f"yaml_{i}",
                    "title": doc.get("title", ""),
                    "content": doc.get("content", ""),
                    "metadata": {"source": str(self.yaml_path.name), "path": doc.get("title", "")}
                })

            self.logger.info(f"Loaded {len(self.documents)} YAML sections from {self.yaml_path}")

        except Exception as e:
            self.logger.error(f"Failed to load YAML reference: {e}")
            self.documents = []

    def retrieve_relevant_content(self, query: str, top_k: int = None,
                                  similarity_threshold: float = None) -> List[Dict[str, Any]]:
        """Retrieve YAML sections that best match the query using simple token matching."""
        if not query or not query.strip():
            return []

        top_k = top_k or self.config.RAG_TOP_K

        q = query.lower()
        tokens = [t for t in q.split() if len(t) > 2]

        scored = []
        for doc in self.documents:
            content = (doc.get("content") or "").lower()
            score = 0
            for t in tokens:
                if t in content:
                    score += content.count(t)

            # Also check title
            title = (doc.get("title") or "").lower()
            for t in tokens:
                if t in title:
                    score += 2

            if score > 0:
                scored.append({"content": doc["content"], "metadata": doc["metadata"], "similarity_score": float(score)})

        # If nothing matched, return a set of general sections (top_k)
        if not scored:
            # return first top_k documents as fallback
            fallback = [
                {"content": d["content"], "metadata": d["metadata"], "similarity_score": 0.0}
                for d in self.documents[:top_k]
            ]
            return fallback

        # Sort by score descending and return top_k
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    def refresh_vector_store(self) -> bool:
        """Reload YAML content (keeps method name for compatibility)."""
        try:
            self.documents = []
            self._load_yaml()
            return True
        except Exception as e:
            self.logger.error(f"Failed to refresh YAML retriever: {e}")
            return False

    def add_new_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Add an in-memory document (does not persist to YAML file)."""
        try:
            new_id = f"custom_{len(self.documents)}"
            self.documents.append({"id": new_id, "title": metadata.get("title", new_id), "content": content, "metadata": metadata})
            return True
        except Exception as e:
            self.logger.error(f"Failed to add new in-memory document: {e}")
            return False

    def search_by_keywords(self, keywords: List[str], top_k: int = None) -> List[Dict[str, Any]]:
        """Convenience wrapper to search by keywords."""
        if not keywords:
            return []
        return self.retrieve_relevant_content(" ".join(keywords), top_k=top_k)

    def get_document_stats(self) -> Dict[str, Any]:
        """Return simple stats about loaded YAML sections."""
        return {
            "total_sections": len(self.documents),
            "source": str(self.yaml_path.name)
        }

    def identify_content_gaps(self, recent_queries: List[str]) -> Dict[str, Any]:
        """Identify queries that returned few or no matches."""
        low_result_queries = []
        for q in recent_queries:
            results = self.retrieve_relevant_content(q, top_k=3)
            if not results or all(r.get("similarity_score", 0) == 0 for r in results):
                low_result_queries.append({"query": q, "result_count": len(results)})

        return {
            "potential_gaps": low_result_queries,
            "gap_count": len(low_result_queries),
            "total_queries_analyzed": len(recent_queries)
        }