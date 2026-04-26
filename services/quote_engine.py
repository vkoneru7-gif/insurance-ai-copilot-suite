def calculate_quote_risk(age, accidents, prior_claims, vehicle_type):
    base_score = 20

    accidents_score = accidents * 40
    claims_score = prior_claims * 25

    if age < 25:
        age_score = 20
    elif age > 70:
        age_score = 15
    else:
        age_score = 0

    high_risk_vehicles = ["Sports Car", "Luxury SUV"]

    if vehicle_type in high_risk_vehicles:
        vehicle_score = 20
    else:
        vehicle_score = 0

    raw_score = (
        base_score +
        accidents_score +
        claims_score +
        age_score +
        vehicle_score
    )

    risk_score = min(raw_score, 100)

    if risk_score >= 80:
        risk_level = "High"
        route = "Senior UW Review"
        human_review_required = "Yes"
    elif risk_score >= 50:
        risk_level = "Medium"
        route = "Standard UW"
        human_review_required = "Yes"
    else:
        risk_level = "Low"
        route = "Fast-Track"
        human_review_required = "No"

    return {
        "risk_score": risk_score,
        "raw_score": raw_score,
        "risk_level": risk_level,
        "route": route,
        "human_review_required": human_review_required,
        "base_score": base_score,
        "accidents_score": accidents_score,
        "claims_score": claims_score,
        "age_score": age_score,
        "vehicle_score": vehicle_score
    }