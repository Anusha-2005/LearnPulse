import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.config import get_settings

try:
    from langchain_core.messages import AIMessage
    LANGCHAIN_MESSAGES_AVAILABLE = True
except ImportError:
    LANGCHAIN_MESSAGES_AVAILABLE = False

client = TestClient(app)

@pytest.fixture
def sample_payload():
    return {
        "performance_data": {
            "student_id": "S123",
            "name": "Alex Student",
            "gpa_history": [3.6, 3.4, 3.1],
            "attendance_rate": 72.5,
            "lms_score": 64.0,
            "avg_assignment_score": 68.0,
            "avg_quiz_score": 62.0
        },
        "prediction": {
            "risk_score": 82.5,
            "risk_level": "High"
        },
        "shap_values": {
            "feature_importance": {
                "attendance_rate": 0.45,
                "avg_assignment_score": 0.35,
                "avg_quiz_score": 0.20
            }
        }
    }

def test_insights_fallback_no_key(sample_payload):
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", None):
        response = client.post("/api/ai/insights", json=sample_payload)
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "risk_explanation" in data
        assert "recommendations" in data
        assert data["provider"] == "fallback-rules"
        assert "Alex Student" in data["summary"]
        # Rule-based fallback checks
        assert any("attendance" in r.lower() for r in data["recommendations"])

@pytest.mark.skipif(not LANGCHAIN_MESSAGES_AVAILABLE, reason="Langchain package not installed locally yet")
@patch("langchain_google_genai.ChatGoogleGenerativeAI.invoke")
def test_insights_gemini_success(mock_invoke, sample_payload):
    # Mock LangChain response
    mock_invoke.return_value = AIMessage(
        content='{"summary": "Alex is showing declining GPA and attendance.", "risk_explanation": "His risk score is driven by low attendance and assignment scores.", "recommendations": ["Improve attendance", "Submit pending work"]}'
    )
    
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", "mock-gemini-key"):
        response = client.post("/api/ai/insights", json=sample_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Alex is showing declining GPA and attendance."
        assert data["risk_explanation"] == "His risk score is driven by low attendance and assignment scores."
        assert "Improve attendance" in data["recommendations"]
        assert data["provider"] == "langchain-gemini"

@pytest.mark.skipif(not LANGCHAIN_MESSAGES_AVAILABLE, reason="Langchain package not installed locally yet")
@patch("langchain_google_genai.ChatGoogleGenerativeAI.invoke")
def test_insights_gemini_api_failure_fallback(mock_invoke, sample_payload):
    # Mock LangChain response raising API error
    mock_invoke.side_effect = Exception("Gemini service quota exceeded")
    
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", "mock-gemini-key"):
        response = client.post("/api/ai/insights", json=sample_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "fallback-rules"
        assert "Alex Student" in data["summary"]
