import json
from django.conf import settings
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)

def build_prompt(resume_text: str) -> str:
    return f"""
You are an expert resume reviewer and career coach for fresh graduates.
Analyze this resume and return JSON with:
- ats_score (0-100)
- missing_sections
- skills_detected
- weaknesses
- suggestions
- rewrites

Resume:
{resume_text}

Return only valid JSON.
"""

def analyze_resume(resume_text: str) -> dict:
    prompt = build_prompt(resume_text)
    resp = genai.generate_text(model="gemini-1.5-pro", prompt=prompt, max_output_tokens=800)
    try:
        return json.loads(resp.text)
    except Exception:
        raise ValueError("Gemini returned invalid JSON: " + resp.text)
