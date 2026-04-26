from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time

from services.gemini_service import generate_policy_summary
from services.security import run_security_screening
from services.quote_engine import calculate_quote_risk
from services.claims_engine import analyze_claim_text
from services.retrieval_engine import search_policy_documents
from database import initialize_database, get_all_workflow_events, save_workflow_event

app = FastAPI(
    title="Insurance AI Copilot Suite API",
    description="REST API backend for the Insurance AI Copilot Suite prototype.",
    version="4.0.0"
)

initialize_database()


class QuoteRequest(BaseModel):
    customer_name: str
    age: int
    state: str
    vehicle_type: str
    accidents: int
    prior_claims: int


class ClaimRequest(BaseModel):
    customer_name: str
    claim_text: str


class RetrievalRequest(BaseModel):
    question: str


class WorkflowRequest(BaseModel):
    customer_name: str
    age: int
    vehicle_type: str
    accidents: int
    prior_claims: int
    claim_text: str
    question: str


@app.get("/")
def root():
    return {
        "message": "Insurance AI Copilot Suite API is running",
        "version": "4.0.0",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "insurance-ai-copilot-api"
    }


@app.post("/quote")
def create_quote(request: QuoteRequest):
    result = calculate_quote_risk(
        age=request.age,
        accidents=request.accidents,
        prior_claims=request.prior_claims,
        vehicle_type=request.vehicle_type
    )

    return {
        "customer_name": request.customer_name,
        "state": request.state,
        "decision": result
    }


@app.post("/claim")
def analyze_claim(request: ClaimRequest):
    result = analyze_claim_text(request.claim_text)

    return {
        "customer_name": request.customer_name,
        "claim_analysis": result
    }


@app.post("/retrieve")
def retrieve_policy_answer(request: RetrievalRequest):
    start_time = time.time()
    provider_used = "gemini"
    fallback_used = False

    security_result = run_security_screening(request.question)

    if not security_result["allowed"]:
        save_workflow_event(
            event_type="Security Event",
            request_id="SEC-" + str(uuid.uuid4())[:8].upper(),
            module_name="Security Guard",
            risk_level="High",
            route="Blocked Request",
            confidence=100,
            escalation_flag="Yes",
            human_review_required="Yes",
            latency_seconds=0.2,
            status="Blocked",
            notes=f"Prompt injection detected: {', '.join(security_result['matched_patterns'])}"
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "question": request.question,
            "status": "blocked",
            "reason": "Potential prompt injection detected.",
            "matched_patterns": security_result["matched_patterns"],
            "provider_used": "security_guard",
            "fallback_used": False,
            "latency_ms": latency_ms
        }

    safe_question = security_result["redacted_text"]

    if safe_question != request.question:
        save_workflow_event(
            event_type="Security Event",
            request_id="SEC-" + str(uuid.uuid4())[:8].upper(),
            module_name="Security Guard",
            risk_level="Medium",
            route="PII Redaction",
            confidence=100,
            escalation_flag="No",
            human_review_required="No",
            latency_seconds=0.2,
            status="Completed",
            notes="PII detected and redacted before retrieval processing."
        )

    results = search_policy_documents(safe_question)

    if not results:
        latency_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "question": request.question,
            "confidence": "Low",
            "message": "No matching policy documents found.",
            "results": [],
            "provider_used": "retrieval_only",
            "fallback_used": False,
            "latency_ms": latency_ms,
            "security": {
                "pii_redacted": safe_question != request.question,
                "screened": True
            }
        }

    top_result = results[0]

    grounded_context = (
        f"Source: {top_result['title']}\n"
        f"Snippet: {top_result['snippet']}\n"
        f"Policy Answer: {top_result['answer']}"
    )

    try:
        llm_summary = generate_policy_summary(
            question=safe_question,
            grounded_context=grounded_context
        )
        llm_status = "success"

    except Exception:
        llm_summary = "LLM summary unavailable. Returning rule-based grounded answer only."
        llm_status = "fallback_used_provider_unavailable_or_quota_limited"
        provider_used = "fallback"
        fallback_used = True

    latency_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "question": request.question,
        "safe_question_used_for_llm": safe_question,
        "confidence": "High" if top_result["score"] >= 75 else "Medium",
        "top_answer": top_result["answer"],
        "llm_summary": llm_summary,
        "llm_status": llm_status,
        "provider_used": provider_used,
        "fallback_used": fallback_used,
        "latency_ms": latency_ms,
        "top_source": top_result["title"],
        "results": results,
        "security": {
            "pii_redacted": safe_question != request.question,
            "screened": True
        }
    }


@app.get("/events")
def get_events():
    rows = get_all_workflow_events()

    events = []

    for row in rows:
        events.append({
            "id": row[0],
            "event_type": row[1],
            "request_id": row[2],
            "timestamp": row[3],
            "module_name": row[4],
            "risk_level": row[5],
            "route": row[6],
            "confidence": row[7],
            "escalation_flag": row[8],
            "human_review_required": row[9],
            "latency_seconds": row[10],
            "status": row[11],
            "notes": row[12]
        })

    return {
        "total_events": len(events),
        "events": events
    }


@app.post("/workflow")
def run_workflow(request: WorkflowRequest):
    request_id = "WF-" + str(uuid.uuid4())[:8].upper()

    quote_result = calculate_quote_risk(
        age=request.age,
        accidents=request.accidents,
        prior_claims=request.prior_claims,
        vehicle_type=request.vehicle_type
    )

    claim_result = analyze_claim_text(request.claim_text)

    retrieval_results = search_policy_documents(request.question)

    top_source = retrieval_results[0]["title"] if retrieval_results else "No matching source found"
    top_answer = retrieval_results[0]["answer"] if retrieval_results else "No grounded answer available"

    human_review_required = (
        quote_result["human_review_required"] == "Yes"
        or claim_result["human_review_required"] == "Yes"
        or not retrieval_results
    )

    final_route = "Human Review Queue" if human_review_required else "Straight-Through Processing"

    save_workflow_event(
        event_type="Orchestrated Workflow",
        request_id=request_id,
        module_name="AI Orchestrator API",
        risk_level=quote_result["risk_level"],
        route=final_route,
        confidence=75 if retrieval_results else 40,
        escalation_flag="Yes" if human_review_required else "No",
        human_review_required="Yes" if human_review_required else "No",
        latency_seconds=2.4,
        status="Completed",
        notes="Workflow executed through quote, claim, and retrieval services."
    )

    return {
        "request_id": request_id,
        "customer_name": request.customer_name,
        "workflow_status": "Completed",
        "services_executed": [
            "Quote Risk Engine",
            "Claims Triage Engine",
            "Policy Retrieval Engine",
            "Audit Event Logger"
        ],
        "final_route": final_route,
        "human_review_required": "Yes" if human_review_required else "No",
        "quote_decision": quote_result,
        "claim_decision": claim_result,
        "retrieval": {
            "top_source": top_source,
            "top_answer": top_answer,
            "results": retrieval_results
        }
    }