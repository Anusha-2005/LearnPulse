import httpx
from typing import Optional
from loguru import logger
from app.config import get_settings

settings = get_settings()

def generate_llm_insight(prompt: str, provider: Optional[str] = None, model: Optional[str] = None) -> Optional[str]:
    """
    Sends a prompt to the configured LLM provider (Gemini or OpenAI) via raw HTTP REST call.
    Returns the text generation response or None if there was an error.
    """
    provider = (provider or settings.llm_provider or "gemini").lower()
    
    # 1. Google Gemini Provider
    if provider == "gemini":
        key = settings.gemini_api_key
        if not key:
            logger.warning("Gemini API key is not configured.")
            return None
            
        model = model or settings.llm_model or "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        try:
            logger.info(f"Calling Gemini API (model: {model})...")
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                # Extract response text
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
        except Exception as e:
            logger.error(f"Gemini API generation failed: {e}")
            return None
            
    # 2. OpenAI Provider
    elif provider == "openai":
        key = settings.openai_api_key
        if not key:
            logger.warning("OpenAI API key is not configured.")
            return None
            
        model = model or settings.llm_model or "gpt-4o-mini"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            logger.info(f"Calling OpenAI API (model: {model})...")
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                # Extract response text
                text = data["choices"][0]["message"]["content"]
                return text.strip()
        except Exception as e:
            logger.error(f"OpenAI API generation failed: {e}")
            return None
            
    else:
        logger.warning(f"Unsupported LLM provider requested: {provider}")
        return None
