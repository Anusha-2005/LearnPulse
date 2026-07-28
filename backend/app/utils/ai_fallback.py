from typing import List, Dict, Any

def generate_heuristic_academic_insight(
    performance_data: Dict[str, Any],
    prediction: Dict[str, Any],
    shap_values: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generates a structured rule-based/heuristic explanation for a student's performance,
    acting as a fallback when the LLM is unavailable.
    """
    name = performance_data.get("name", "Student")
    gpa_history = performance_data.get("gpa_history", [])
    attendance = performance_data.get("attendance_rate", 100.0)
    assignment = performance_data.get("avg_assignment_score", 100.0)
    quiz = performance_data.get("avg_quiz_score", 100.0)
    
    risk_level = prediction.get("risk_level", "Low")
    risk_score = prediction.get("risk_score", 0.0)
    
    feature_importance = shap_values.get("feature_importance", {})

    # 1. Generate Summary
    gpa_trend = "stable"
    if len(gpa_history) >= 2:
        diff = gpa_history[-1] - gpa_history[0]
        if diff < -0.15:
            gpa_trend = "declining"
        elif diff > 0.15:
            gpa_trend = "improving"
            
    latest_gpa = gpa_history[-1] if gpa_history else 0.0
    summary = (
        f"{name} currently maintains a {latest_gpa:.2f} GPA, which has been relatively {gpa_trend} "
        f"over the past semesters. They are classified as a {risk_level} Risk student with a risk score of {risk_score:.1f}%."
    )

    # 2. Risk Explanation (Identify key drivers)
    drivers = []
    # Identify key features from SHAP values if present
    if feature_importance:
        # Sort features by SHAP value descending (higher SHAP = higher risk contribution)
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        top_features = [feat for feat, val in sorted_features[:2] if val > 0]
        if top_features:
            drivers.extend(top_features)

    # Fallback to general metrics if no SHAP features contributed
    if not drivers:
        if attendance < 75.0:
            drivers.append("attendance_rate")
        if assignment < 70.0:
            drivers.append("avg_assignment_score")
        if quiz < 70.0:
            drivers.append("avg_quiz_score")

    # Map database keys to human friendly names
    name_map = {
        "attendance_rate": "low class attendance",
        "avg_assignment_score": "poor assignment completion",
        "avg_quiz_score": "low quiz scores",
        "gpa_history": "declining GPA trend",
        "lms_score": "low LMS engagement"
    }
    
    friendly_drivers = [name_map.get(d, d.replace("_", " ")) for d in drivers]

    if friendly_drivers:
        explanation = (
            f"The primary academic factors driving {name}'s risk score are "
            f"{', '.join(friendly_drivers[:-1]) + ' and ' + friendly_drivers[-1] if len(friendly_drivers) > 1 else friendly_drivers[0]}. "
            f"These areas require immediate intervention."
        )
    else:
        explanation = (
            f"{name}'s academic metrics are within the standard range. The primary recommendation is "
            "to continue tracking attendance and assignment progress."
        )

    # 3. Personalised Recommendations
    recommendations = []
    if attendance < 75.0:
        recommendations.append(f"Improve class attendance to at least 85% to ensure full comprehension of lectures.")
    if assignment < 70.0:
        recommendations.append(f"Request support for upcoming assignments and complete any outstanding/late submissions.")
    if quiz < 70.0:
        recommendations.append(f"Attend tutor-led revision sessions to strengthen understanding of key quiz concepts.")
    if gpa_trend == "declining":
        recommendations.append(f"Schedule a one-on-one session with the academic advisor to draft a study progress recovery plan.")
        
    if not recommendations:
        recommendations.append("Continue maintaining the current study rhythm and attend regular lecture sessions.")

    return {
        "summary": summary,
        "risk_explanation": explanation,
        "recommendations": recommendations,
        "provider": "fallback-rules"
    }
