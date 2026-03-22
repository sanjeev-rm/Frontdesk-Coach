# Setup & Configuration

## Prerequisites

- Python 3.8+
- API access to an LLM provider (OpenAI, Anthropic, or Cornell's endpoint)

## Installation

```bash
git clone https://github.com/sanjeev-rm/Frontdesk-Coach.git
cd Frontdesk-Coach
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment

```bash
cp .env.template .env
```

Edit `.env` with your values:

```env
LLM_API_URL=https://api.ai.it.cornell.edu
LLM_API_KEY=your_api_key_here

FAST_MODEL=gpt-3.5-turbo
BALANCED_MODEL=gpt-4
SMART_MODEL=gpt-4
DEFAULT_MODEL=gpt-4

EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_API_URL=https://api.ai.it.cornell.edu
```

## Model Configuration

Use cheaper/faster models for agents that don't need deep reasoning:

```env
FAST_MODEL=gpt-3.5-turbo      # Guest agent responses
BALANCED_MODEL=gpt-4           # Guest interactions
SMART_MODEL=gpt-4              # Coaching + reports
```

## Retrieval Configuration

Controls how much of the training YAML is pulled into each coaching response:

```env
RAG_TOP_K=5          # Number of YAML sections retrieved per query
CHUNK_SIZE=1000      # Token chunk size for document processor
CHUNK_OVERLAP=200    # Overlap between chunks
```

## Other Settings

```env
DEBUG=false
SESSION_TIMEOUT_MINUTES=60
MAX_MESSAGE_HISTORY=50
LOG_LEVEL=INFO
MAX_DOCUMENT_SIZE_MB=10
```

## Running

```bash
streamlit run app.py
```

App runs at `http://localhost:8501`.

## Training Manual

The system uses `hotel_training_reference.yaml` as the single source of truth for coaching and evaluation. Update this file to reflect your hotel's actual standards — agents will automatically use the new content on next startup.
