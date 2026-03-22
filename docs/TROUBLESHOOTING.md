# Troubleshooting

## API Errors

**Connection refused / auth errors**
- Double-check `LLM_API_URL` and `LLM_API_KEY` in `.env`
- Test your API key independently before running the app

## No Training Content Loading

- Confirm `hotel_training_reference.yaml` exists in the project root
- Check `config/settings.py` for the `TRAINING_DOCS_PATH` value
- Look at `logs/` for retriever errors on startup

## Slow Responses

- Set `FAST_MODEL=gpt-3.5-turbo` for the Guest Agent to speed up roleplay turns
- Lower `RAG_TOP_K` to reduce retrieval overhead
- Reduce `CHUNK_SIZE` if document processing is the bottleneck

## Memory / Performance

- Lower `MAX_MESSAGE_HISTORY` to reduce context size per call
- Clear and reinitialize the retriever if stale:

```python
from rag_system.retriever import RAGRetriever
from config.settings import AppConfig
rag = RAGRetriever(AppConfig())
rag.refresh_vector_store()
```

## Document Processing

**File too large** — increase `MAX_DOCUMENT_SIZE_MB` in `.env`

**Encoding errors** — convert source files to UTF-8; the processor tries common encodings automatically

**Unsupported format** — convert the file to `.pdf`, `.docx`, or `.txt`

## Logs

All logs are in `logs/`:
- `hotel_training_YYYYMMDD.log` — general output
- `hotel_training_errors_YYYYMMDD.log` — errors only

Set `LOG_LEVEL=DEBUG` in `.env` for verbose output.
