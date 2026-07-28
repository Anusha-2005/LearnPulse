from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from loguru import logger

from app.config import get_settings
from app.utils.ai_fallback import generate_heuristic_academic_insight

# Try loading LangChain dependencies; define placeholder check if missing
try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LangChain libraries not loaded: {e}. Falling back to rule-based insights.")
    LANGCHAIN_AVAILABLE = False

router = APIRouter(prefix="/ai", tags=["AI"])
settings = get_settings()

# Request schemas
class StudentPerformanceInput(BaseModel):
    student_id: str
    name: str
    gpa_history: List[float]
    attendance_rate: float
    lms_score: float
    avg_assignment_score: float
    avg_quiz_score: float

class PredictionResult(BaseModel):
    risk_score: float
    risk_level: str

class SHAPValuesInput(BaseModel):
    feature_importance: Dict[str, float]

class AIInsightRequest(BaseModel):
    performance_data: StudentPerformanceInput
    prediction: PredictionResult
    shap_values: SHAPValuesInput

# Response schemas
class AIInsightResponse(BaseModel):
    summary: str
    risk_explanation: str
    recommendations: List[str]
    provider: str

# Expected JSON schema for LangChain output parsing
if LANGCHAIN_AVAILABLE:
    class StudentAIResponse(BaseModel):
        summary: str = Field(description="A concise 1-2 sentence academic summary of the student's status and trajectory.")
        risk_explanation: str = Field(description="An explanation of why the student has their risk score, highlighting the primary risk drivers.")
        recommendations: List[str] = Field(description="A list of 2-3 specific, actionable recommendations for the student to improve.")

@router.post("/insights", response_model=AIInsightResponse)
def get_student_insights(payload: AIInsightRequest):
    """
    Generate personalised student academic insights, risk explanations, and recommendations
    using Google Gemini API via LangChain. Falls back to a local heuristic-based summary
    if Gemini/LangChain is unavailable or the API call fails.
    """
    perf = payload.performance_data.dict()
    pred = payload.prediction.dict()
    shap = payload.shap_values.dict()

    # Graceful fallback check if Gemini API key is missing or LangChain is not imported
    if not LANGCHAIN_AVAILABLE or not settings.gemini_api_key:
        logger.info("LangChain or Gemini API Key unavailable. Generating rule-based fallback insights.")
        fallback_data = generate_heuristic_academic_insight(perf, pred, shap)
        return fallback_data

    try:
        # 1. Initialize LangChain Google Gemini Model
        model = ChatGoogleGenerativeAI(
            api_key=settings.gemini_api_key,
            model="gemini-3.1-flash-lite",
            temperature=0.2,
            timeout=15.0
        )

        # 2. Setup JSON Output Parser
        parser = JsonOutputParser(pydantic_object=StudentAIResponse)

        # 3. Create Advisor Advisor Prompt Template
        prompt_template = PromptTemplate(
            template="You are an expert AI academic advisor helping university students improve their performance.\n"
                     "Analyze the following student data, prediction results, and SHAP feature importance values.\n\n"
                     "Student Performance Data:\n"
                     "- Name: {name}\n"
                     "- GPA history: {gpa_history}\n"
                     "- Attendance Rate: {attendance_rate}%\n"
                     "- LMS Score: {lms_score}\n"
                     "- Avg Assignment Score: {avg_assignment_score}%\n"
                     "- Avg Quiz Score: {avg_quiz_score}%\n\n"
                     "Model Prediction Results:\n"
                     "- Risk Score (Probability of Dropout): {risk_score}%\n"
                     "- Predicted Risk Level: {risk_level}\n\n"
                     "SHAP Feature Importance (Higher positive values indicate a higher contribution to the risk level):\n"
                     "{shap_importance}\n\n"
                     "Generate a structured response according to the formatting instructions below.\n\n"
                     "{format_instructions}\n",
            input_variables=["name", "gpa_history", "attendance_rate", "lms_score", "avg_assignment_score", "avg_quiz_score", "risk_score", "risk_level", "shap_importance"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        # 4. Construct LCEL Chain
        chain = prompt_template | model | parser

        # 5. Format SHAP importance dictionary to readable string
        shap_str = "\n".join([f"- {k}: {v:.4f}" for k, v in payload.shap_values.feature_importance.items()])

        # 6. Execute Chain
        logger.info(f"Calling Gemini via LangChain for student: {payload.performance_data.name}...")
        result = chain.invoke({
            "name": payload.performance_data.name,
            "gpa_history": str(payload.performance_data.gpa_history),
            "attendance_rate": payload.performance_data.attendance_rate,
            "lms_score": payload.performance_data.lms_score,
            "avg_assignment_score": payload.performance_data.avg_assignment_score,
            "avg_quiz_score": payload.performance_data.avg_quiz_score,
            "risk_score": payload.prediction.risk_score,
            "risk_level": payload.prediction.risk_level,
            "shap_importance": shap_str
        })

        return AIInsightResponse(
            summary=result.get("summary", ""),
            risk_explanation=result.get("risk_explanation", ""),
            recommendations=result.get("recommendations", []),
            provider="langchain-gemini"
        )

    except Exception as e:
        logger.error(f"Gemini LangChain invocation failed: {e}. Falling back to rule-based insights.")
        fallback_data = generate_heuristic_academic_insight(perf, pred, shap)
        return fallback_data
