POLICY_DOCUMENTS = [
    {
        "title": "Auto Policy Section 4.2 — Collision Coverage",
        "keywords": ["collision", "accident", "crash", "rear-end", "vehicle damage", "damage"],
        "snippet": "Collision coverage may apply when an insured vehicle is damaged due to impact with another vehicle or object, subject to deductible and active policy status.",
        "answer": "Collision damage may be covered if the customer carries collision coverage. Final payout depends on deductible, exclusions, and whether the policy was active at the time of loss."
    },
    {
        "title": "Claims Handbook Section 2.1 — Deductibles",
        "keywords": ["deductible", "payment", "payout", "claim payment", "out of pocket"],
        "snippet": "The deductible is the customer responsibility amount subtracted from an approved claim payment before final payout is issued.",
        "answer": "The deductible is the amount the customer must pay before the insurer issues the final approved claim payout."
    },
    {
        "title": "State Rules Addendum — Texas Vehicle Rules",
        "keywords": ["texas", "tx", "state rule", "state rules", "vehicle rules"],
        "snippet": "Texas vehicle claims may require state-specific review depending on coverage type, liability details, and claim documentation.",
        "answer": "Texas vehicle claims may require state-specific review before final claim handling or payout decisions."
    },
    {
        "title": "Rental Reimbursement Section 5.3",
        "keywords": ["rental", "rental car", "replacement car", "temporary vehicle"],
        "snippet": "Rental reimbursement may apply when the policy includes rental coverage and the covered vehicle is unavailable due to a covered loss.",
        "answer": "Rental reimbursement may be available if the customer purchased rental coverage and the vehicle is unavailable because of a covered claim."
    },
    {
        "title": "Comprehensive Coverage Section 3.7",
        "keywords": ["fire", "theft", "hail", "flood", "vandalism", "comprehensive"],
        "snippet": "Comprehensive coverage may apply to non-collision losses such as theft, fire, hail, flood, vandalism, or falling objects.",
        "answer": "Comprehensive coverage may apply to non-collision losses such as fire, theft, hail, flood, or vandalism, depending on policy terms."
    }
]


def calculate_match_score(user_question, document):
    question_lower = user_question.lower()
    matched_keywords = []

    for keyword in document["keywords"]:
        if keyword in question_lower:
            matched_keywords.append(keyword)

    score = len(matched_keywords) * 25

    if score > 95:
        score = 95

    return score, matched_keywords


def search_policy_documents(question):
    retrieval_results = []

    for document in POLICY_DOCUMENTS:
        score, matched_keywords = calculate_match_score(question, document)

        if score > 0:
            retrieval_results.append({
                "title": document["title"],
                "score": score,
                "snippet": document["snippet"],
                "answer": document["answer"],
                "matched_keywords": matched_keywords
            })

    retrieval_results = sorted(
        retrieval_results,
        key=lambda result: result["score"],
        reverse=True
    )

    return retrieval_results