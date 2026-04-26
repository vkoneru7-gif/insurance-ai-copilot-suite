import re


SUSPICIOUS_PROMPT_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal system prompt",
    "show hidden prompt",
    "bypass policy",
    "bypass safety",
    "override instructions",
    "act as developer",
    "act as system",
    "jailbreak",
    "do anything now",
    "disable guardrails",
    "show confidential data",
    "leak private information"
]


def detect_prompt_injection(text):
    """
    Detects simple prompt injection attempts in user-provided text.
    Returns a dictionary with whether the text is suspicious and which patterns matched.
    """
    if not text:
        return {
            "is_suspicious": False,
            "matched_patterns": []
        }

    lowered_text = text.lower()
    matched_patterns = []

    for pattern in SUSPICIOUS_PROMPT_PATTERNS:
        if pattern in lowered_text:
            matched_patterns.append(pattern)

    return {
        "is_suspicious": len(matched_patterns) > 0,
        "matched_patterns": matched_patterns
    }


def redact_pii(text):
    """
    Redacts common sensitive information before text is sent to downstream AI systems.
    This is prototype-level redaction, not a replacement for enterprise DLP tools.
    """
    if not text:
        return text

    redacted_text = text

    redacted_text = re.sub(
        r"\b\d{3}-\d{2}-\d{4}\b",
        "[REDACTED_SSN]",
        redacted_text
    )

    redacted_text = re.sub(
        r"\b\d{9}\b",
        "[REDACTED_POSSIBLE_SSN]",
        redacted_text
    )

    redacted_text = re.sub(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "[REDACTED_EMAIL]",
        redacted_text
    )

    redacted_text = re.sub(
        r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "[REDACTED_PHONE]",
        redacted_text
    )

    redacted_text = re.sub(
        r"\b\d{5}(?:-\d{4})?\b",
        "[REDACTED_ZIP]",
        redacted_text
    )

    return redacted_text


def run_security_screening(text):
    """
    Runs all prototype security checks before processing user input.
    """
    injection_result = detect_prompt_injection(text)
    redacted_text = redact_pii(text)

    return {
        "allowed": not injection_result["is_suspicious"],
        "prompt_injection_detected": injection_result["is_suspicious"],
        "matched_patterns": injection_result["matched_patterns"],
        "redacted_text": redacted_text
    }