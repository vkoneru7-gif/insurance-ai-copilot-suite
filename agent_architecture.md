# Agent Architecture — Insurance AI Copilot Suite

## Purpose

This document explains how the current workflow orchestration prototype maps to an enterprise agent-based architecture.

The current implementation does not claim to be a full autonomous agent platform. It is a service-orchestrated agent-style workflow that can evolve into Agent-to-Agent and MCP-based architecture.

## Current Agent-Style Workflow

The current `/workflow` API coordinates multiple domain services:

1. Quote Risk Engine
2. Claims Triage Engine
3. Policy Retrieval Engine
4. Security Guard
5. Audit Event Logger

Each service has a focused responsibility and returns structured output.

## Current Flow

```text
User Request
   ↓
FastAPI /workflow
   ↓
Quote Risk Engine
   ↓
Claims Triage Engine
   ↓
Policy Retrieval Engine
   ↓
Audit Event Logger
   ↓
Final Human Review / Straight-Through Routing Decision