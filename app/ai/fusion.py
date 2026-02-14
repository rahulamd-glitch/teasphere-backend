def fuse_decision(ai_result, hit_result):

    disease = ai_result["disease"]
    conf = ai_result["confidence"]

    # ✅ CORRECT PATH FROM HIT RESULT
    features = hit_result.get("features", {})

    g = features.get("green_ratio", 0)
    b = features.get("brown_ratio", 0)
    r = features.get("red_ratio", 0)
    s = features.get("spot_density", 0)

    reasons = []

    # ===== FUSION LOGIC =====

    # 1. AI says brown but leaf mostly green → override to healthy
    if disease == "brown blight" and conf < 70:
        if g > 0.60 and b < 0.12:
            disease = "healthy"
            reasons.append("High green & low brown → healthy override")

    # 2. AI says brown but strong red → red rust
    if disease == "brown blight" and r > 0.18:
        disease = "red rust"
        reasons.append("Strong red hue → red rust")

    # 3. Strong texture spots → blister
    if s > 0.22 and b < 0.10:
        disease = "blister blight"
        reasons.append("High spot texture → blister blight")

    # 4. If HIT is very confident, trust HIT
    if hit_result.get("hit_confidence", 0) > 80:
        disease = hit_result.get("hit_disease", disease)
        reasons.append("HIT high confidence override")

    return {
        "disease": disease,
        "confidence": conf,
        "reasons": reasons,
        "ai": ai_result,
        "hit": hit_result
    }
