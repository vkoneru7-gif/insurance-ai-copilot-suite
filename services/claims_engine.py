def analyze_claim_text(claim_text):
    text = claim_text.lower()

    high_words = [
        "injury",
        "injured",
        "hospital",
        "ambulance",
        "fire",
        "total loss",
        "bleeding",
        "airbag",
        "fire department"
    ]

    medium_words = [
        "accident",
        "collision",
        "rear-end",
        "damage",
        "dent",
        "crash",
        "tow",
        "towed",
        "non-drivable",
        "not drivable"
    ]

    low_words = [
        "minor",
        "scratch",
        "parking lot",
        "small"
    ]

    escalation_rules = {
        "Possible Injury": ["injury", "injured", "hospital", "ambulance", "bleeding"],
        "Fire Department Response": ["fire department", "fire truck", "firefighters"],
        "Non-Drivable Vehicle": ["non-drivable", "not drivable", "towed", "tow truck"],
        "Minor Child Passenger": ["child", "minor passenger", "baby", "infant", "kid"],
        "Possible Fraud Indicator": ["staged", "suspicious", "changed story", "inconsistent", "late report"],
        "Intoxicated Driver": ["drunk", "intoxicated", "dui", "alcohol"]
    }

    detected_urgency_signals = []

    for word in high_words:
        if word in text:
            detected_urgency_signals.append(word)

    for word in medium_words:
        if word in text:
            detected_urgency_signals.append(word)

    for word in low_words:
        if word in text:
            detected_urgency_signals.append(word)

    escalation_flags = []

    for flag_name, keywords in escalation_rules.items():
        for keyword in keywords:
            if keyword in text:
                escalation_flags.append(flag_name)
                break

    if any(word in text for word in high_words) or escalation_flags:
        urgency = "High"
    elif any(word in text for word in medium_words):
        urgency = "Medium"
    elif any(word in text for word in low_words):
        urgency = "Low"
    else:
        urgency = "Medium"

    missing_items = []

    if "police" not in text and "report" not in text:
        missing_items.append("Police report")

    if "photo" not in text and "picture" not in text and "image" not in text:
        missing_items.append("Damage photos")

    if "estimate" not in text and "repair" not in text:
        missing_items.append("Repair estimate")

    if "location" not in text and "street" not in text and "road" not in text and "parking lot" not in text:
        missing_items.append("Loss location")

    if "date" not in text and "today" not in text and "yesterday" not in text:
        missing_items.append("Date of loss")

    if urgency == "High":
        recommended_route = "Senior Claims Adjuster"
        human_review_required = "Yes"
    elif urgency == "Medium":
        recommended_route = "Claims Adjuster"
        human_review_required = "Yes"
    else:
        recommended_route = "Fast-Track Claims Queue"
        human_review_required = "No"

    return {
        "urgency": urgency,
        "detected_urgency_signals": detected_urgency_signals,
        "escalation_flags": escalation_flags,
        "missing_items": missing_items,
        "recommended_route": recommended_route,
        "human_review_required": human_review_required
    }