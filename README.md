# Insurance AI Copilot Suite

Enterprise-grade Generative AI platform prototype for insurance operations.

This project demonstrates how an insurance company can use secure AI workflows, LLM integrations, retrieval systems, orchestration services, and cloud-ready architecture to improve quote intake, claims triage, policy support, and operational efficiency.

---

# Why This Project Matters

Insurance organizations handle repetitive workflows, document-heavy decisions, customer service requests, and regulated data.

This prototype shows how GenAI can be introduced responsibly through:

- API-first architecture
- secure retrieval before generation
- human-review routing
- audit logging
- workflow orchestration
- cloud deployment readiness

---

# Core Features

## Quote Copilot

- Risk scoring
- Underwriting routing
- Human review escalation
- Structured API response

## Claims Copilot

- Claim text triage
- Urgency detection
- Escalation flags
- Missing information checks

## Policy Retrieval

- Prompt injection screening
- PII redaction
- Grounded retrieval responses
- Gemini LLM summarization with fallback mode

## Workflow Orchestrator

- Multi-service request coordination
- Quote + Claim + Retrieval combined workflow
- Operational traceability

## Audit Events

- Workflow event history
- Local persistence
- Future DynamoDB migration path

---

# Tech Stack

## Backend

- Python
- FastAPI
- Pydantic

## Frontend

- Streamlit (prototype UI)
- React + Next.js migration plan included

## AI / GenAI

- Gemini API
- Retrieval-first response pattern
- Provider fallback handling

## Data

- SQLite (prototype)
- DynamoDB roadmap

## DevOps

- Docker
- GitHub Actions CI
- Pytest automated tests

## Cloud Roadmap

- AWS ECS / Fargate
- API Gateway / ALB
- S3
- OpenSearch
- CloudWatch
- Secrets Manager
- Amazon Bedrock

---

# API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/quote` | Quote risk decision |
| POST | `/claim` | Claims triage |
| POST | `/retrieve` | Secure retrieval + LLM summary |
| POST | `/workflow` | Multi-service orchestration |
| GET | `/events` | Audit event history |

---

# Local Run Instructions

## Install Dependencies

```bash
pip install -r requirements.txt

Create Environment File
GEMINI_API_KEY=your_key_here
Start Backend
python -m uvicorn api:app --reload

Swagger Docs:

http://127.0.0.1:8000/docs
Start Frontend
python -m streamlit run app.py

UI:

http://localhost:8501
Testing

Run automated API tests:

python -m pytest -v

Current coverage includes:

health endpoint
quote endpoint
claim endpoint
retrieval security blocking
workflow orchestration
Docker

Run backend in containerized mode:

docker build -t insurance-ai-api .
docker run -p 8000:8000 insurance-ai-api
Security Controls
Prompt injection detection
PII redaction before model calls
Deterministic fallback responses
Audit logging
Human review escalation path
Architecture Documents Included
architecture.md
agent_architecture.md
aws_deployment.md
frontend-plan.md
Honest Current Status

Implemented:

Working FastAPI backend
Working Streamlit frontend
Gemini integration
Security controls
Automated tests
CI/CD pipeline
Docker containerization
AWS deployment roadmap

Not Yet Implemented:

Live AWS deployment
Real vector database retrieval
Authentication / RBAC
Full React frontend