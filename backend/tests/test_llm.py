import pytest
from unittest.mock import patch, MagicMock
from app.utils.performance_utils import generate_ai_insight
from app.utils.llm_utils import generate_llm_insight
from app.config import get_settings

def test_generate_ai_insight_fallback_no_keys():
    # Make sure we don't have active keys in default test config
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", None), patch.object(settings, "openai_api_key", None):
        insight = generate_ai_insight(
            student_name="Test Student",
            gpa_series=[3.8, 3.7, 3.5, 3.4],
            failed_subjects_total=0,
            risk_category="Low",
            warnings=[]
        )
        # Should fallback to rule-based string
        assert "Test Student" in insight
        assert "stable" in insight or "decline" in insight
        assert "No critical early-warning flags" in insight

@patch("httpx.Client.post")
def test_generate_llm_insight_gemini_success(mock_post):
    # Mock response for Gemini API
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "This is a mocked Gemini insight for the student."
                        }
                    ]
                }
            }
        ]
    }
    mock_post.return_value = mock_resp
    
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", "mock-gemini-key"), \
         patch.object(settings, "llm_provider", "gemini"):
        
        insight = generate_ai_insight(
            student_name="Test Student",
            gpa_series=[3.5, 3.4],
            failed_subjects_total=2,
            risk_category="Medium",
            warnings=[{"message": "Declining GPA"}]
        )
        assert insight == "This is a mocked Gemini insight for the student."

@patch("httpx.Client.post")
def test_generate_llm_insight_openai_success(mock_post):
    # Mock response for OpenAI API
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a mocked OpenAI insight."
                }
            }
        ]
    }
    mock_post.return_value = mock_resp
    
    settings = get_settings()
    with patch.object(settings, "openai_api_key", "mock-openai-key"), \
         patch.object(settings, "llm_provider", "openai"):
        
        insight = generate_ai_insight(
            student_name="Test Student",
            gpa_series=[3.5, 3.4],
            failed_subjects_total=2,
            risk_category="Medium",
            warnings=[{"message": "Declining GPA"}]
        )
        assert insight == "This is a mocked OpenAI insight."

@patch("httpx.Client.post")
def test_generate_llm_insight_api_failure_fallback(mock_post):
    # Mock response raising an error or returning failure
    mock_post.side_effect = Exception("API connection timed out")
    
    settings = get_settings()
    with patch.object(settings, "gemini_api_key", "mock-gemini-key"), \
         patch.object(settings, "llm_provider", "gemini"):
        
        insight = generate_ai_insight(
            student_name="Test Student",
            gpa_series=[3.8, 3.6],
            failed_subjects_total=3,
            risk_category="High",
            warnings=[{"message": "Failed courses"}]
        )
        # Should fallback to rule-based because API failed
        assert "Test Student" in insight
        assert "failed 3 subjects" in insight
        assert "Immediate academic intervention" in insight
