# Insurance AI Copilot Suite — Architecture

## Current Prototype

The current prototype is a local-first enterprise GenAI platform for insurance operations.

### Components

- Streamlit frontend for demo workflow screens
- FastAPI backend for REST APIs
- SQLite audit database for workflow events
- Modular Python services:
  - Quote risk engine
  - Claims triage engine
  - Policy retrieval engine
  - Security screening service
  - Gemini LLM summary service

### Current API Endpoints

- `GET /health`
- `POST /quote`
- `POST /claim`
- `POST /retrieve`
- `POST /workflow`
- `GET /events`

## Current Request Flow

1. User submits insurance question or workflow request.
2. FastAPI receives request.
3. Security layer screens for prompt injection and PII.
4. Retrieval engine finds relevant policy content.
5. LLM layer attempts grounded summary generation.
6. If LLM provider fails or quota is reached, deterministic fallback is used.
7. Event data is written to SQLite audit logs.
8. API returns structured JSON response.

## AWS Target Architecture

### Frontend

- React + Next.js frontend
- Hosted on AWS Amplify or S3 + CloudFront

### Backend

- FastAPI containerized with Docker
- Deployed to Amazon ECS on AWS Fargate
- API Gateway or Application Load Balancer in front of backend

### LLM Layer

- Amazon Bedrock for managed foundation model inference
- Optional provider abstraction for Gemini, OpenAI, Claude, or Bedrock

### Retrieval / RAG

- Policy documents stored in Amazon S3
- Embeddings generated during document ingestion
- Amazon OpenSearch Service used for vector search
- Retrieved chunks passed to LLM with grounding instructions

### Persistence

- DynamoDB for workflow events, audit logs, request metadata, and session state
- SQLite used only for local prototype development

### Observability

- CloudWatch Logs for API logs
- CloudWatch Metrics for latency, failures, fallback rate, and request volume
- Request IDs included across workflow events

### Security

- Secrets stored in AWS Secrets Manager
- IAM roles for service permissions
- PII redaction before LLM calls
- Prompt injection detection before retrieval/model execution
- Human review routing for risky or low-confidence outputs

## Production Upgrade Roadmap

### Phase 1 — Local Prototype
Completed:
- FastAPI APIs
- Streamlit UI
- SQLite audit logs
- Security screening
- Gemini LLM integration
- fallback handling
- retrieval telemetry

### Phase 2 — Containerization
Next:
- Add Dockerfile
- Run FastAPI in container
- Separate frontend/backend runtime

### Phase 3 — AWS Deployment
Next:
- Deploy FastAPI to ECS/Fargate
- Store secrets in AWS Secrets Manager
- Move logs to CloudWatch

### Phase 4 — Enterprise RAG
Next:
- Move policy documents to S3
- Add embedding pipeline
- Use OpenSearch vector search
- Add top-k retrieval evaluation

### Phase 5 — Production Governance
Next:
- Add automated tests
- Add GitHub Actions CI
- Add model/provider failover
- Add role-based access control