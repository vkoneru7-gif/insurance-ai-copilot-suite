# AWS Deployment Plan — Insurance AI Copilot Suite

## Goal

Deploy the Insurance AI Copilot Suite as an AWS-ready enterprise GenAI platform prototype.

The current system runs locally with FastAPI, Streamlit, SQLite, Gemini API, and modular Python services. The AWS target design separates frontend, backend, retrieval, storage, secrets, and observability.

## Current Local Runtime

- Streamlit frontend runs on `localhost:8501`
- FastAPI backend runs on `localhost:8000`
- SQLite stores workflow events locally
- Gemini API is used for grounded LLM summaries
- `.env` stores local API secrets

## Target AWS Architecture

```text
User
 ↓
CloudFront
 ↓
React / Next.js Frontend
 ↓
API Gateway or Application Load Balancer
 ↓
FastAPI Backend on ECS Fargate
 ↓
Service Layer
 ├── Quote Risk Engine
 ├── Claims Triage Engine
 ├── Retrieval Engine
 ├── Security Guard
 ├── LLM Provider Layer
 └── Audit Logger
 ↓
AWS Services
 ├── Bedrock or external LLM provider
 ├── OpenSearch vector index
 ├── S3 policy document storage
 ├── DynamoDB audit logs
 ├── Secrets Manager
 └── CloudWatch