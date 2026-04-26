# Insurance AI Copilot Suite

A local-first enterprise AI workflow prototype for insurance operations.

## Current V3 Features

- Streamlit executive dashboard
- SQLite persistent workflow audit logs
- Real dashboard metrics from saved workflow events
- Quote Copilot with risk scoring and routing
- Claims Copilot with triage and escalation flags
- Policy Retrieval Engine with confidence scoring
- Modular service layer:
  - quote_engine.py
  - claims_engine.py
  - retrieval_engine.py
- Database layer:
  - database.py

## Architecture

- app.py: Streamlit UI
- database.py: SQLite persistence
- services/: Business logic modules
- tabs/: Future UI tab modules

## Honest Limitations

- Local SQLite only
- No authentication yet
- No FastAPI backend yet
- Retrieval is keyword-based, not vector RAG
- Not deployed yet