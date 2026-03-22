# Architecture

![System Architecture](../assets/system_architecture.png)

## Three Phases

### Phase 1 — System Setup
When the user starts a session, `hotel_training_reference.yaml` is loaded and flattened into searchable sections by the RAG retriever. These sections are made available to the Coach and Report agents for the duration of the session.

### Phase 2 — Interactive Training Loop
The core training loop runs inside a Streamlit interface:

- The **Guest Agent** opens with a realistic scenario (billing dispute, room complaint, etc.) and responds in character as a hotel guest
- The **Human Trainee** types responses as they would at the front desk
- The **Coach Agent** evaluates each trainee response against the training manual and posts live feedback in the sidebar

This loop continues until the trainee ends the session.

### Phase 3 — Analysis & Reporting
After the session ends:

- The full conversation history is passed to the **Report Agent**
- The Report Agent evaluates performance against the training YAML's standards and metrics
- A structured report is generated covering ratings, specific examples, knowledge gaps, and next steps

## Agent Design

All agents extend `BaseAgent` (`agents/base_agent.py`), which handles:
- LLM API calls
- Conversation history management
- Prompt construction

| Agent | File | Model Tier | Role |
|---|---|---|---|
| Guest Agent | `agents/guest_agent.py` | Fast | Scenario simulation |
| Coach Agent | `agents/coach_agent.py` | Smart | Real-time feedback |
| Report Agent | `agents/report_agent.py` | Smart | Session analysis |

## Knowledge Retrieval

The RAG retriever (`rag_system/retriever.py`) reads `hotel_training_reference.yaml` at startup, flattens it into sections, and does keyword-based lookup. Embedding-based vector retrieval is stubbed in `rag_system/` but not active — the YAML retriever is the live path.

## Project Structure

```
Frontdesk-Coach/
├── app.py                        # Streamlit app entrypoint
├── hotel_training_reference.yaml # Primary training knowledge base
├── agents/
│   ├── base_agent.py
│   ├── guest_agent.py
│   ├── coach_agent.py
│   └── report_agent.py
├── rag_system/
│   └── retriever.py              # YAML-backed retriever
├── config/settings.py            # AppConfig
├── utils/
│   ├── logger.py
│   └── session_manager.py
├── assets/                       # Images and static files
├── scripts/                      # Dev utilities (setup, validation, tests)
└── docs/
```
