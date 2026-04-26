# Frontend Plan — React + Next.js

## Goal

The current prototype uses Streamlit for fast local demonstration. The production frontend target is React + Next.js to align with enterprise full-stack requirements.

## Current Frontend

- Streamlit dashboard
- Quote Copilot tab
- Policy Retrieval tab
- Claims Copilot tab
- AI Orchestrator tab

## Target Frontend

- React + Next.js application
- API-first communication with FastAPI backend
- Component-based UI
- Environment-based backend URL
- Production hosting on AWS Amplify or S3 + CloudFront

## Planned Pages

### Dashboard

Shows:

- workflow volume
- human review queue
- average latency
- fallback rate
- security events

### Quote Copilot

Calls:

- `POST /quote`

### Claims Copilot

Calls:

- `POST /claim`

### Policy Retrieval

Calls:

- `POST /retrieve`

### Workflow Orchestrator

Calls:

- `POST /workflow`

### Audit Events

Calls:

- `GET /events`

## Why Next.js

Next.js gives:

- modern React frontend
- production routing
- reusable components
- API integration patterns
- easier deployment to cloud platforms

## Honest Current Status

Implemented:

- Streamlit frontend prototype
- FastAPI backend APIs

Not implemented yet:

- React + Next.js frontend
- authentication
- role-based UI
- production deployment

## Migration Plan

1. Keep Streamlit as demo UI.
2. Create Next.js frontend shell.
3. Connect pages to existing FastAPI endpoints.
4. Add authentication.
5. Deploy frontend separately from backend.