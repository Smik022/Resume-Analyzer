import os
import json
from dotenv import load_dotenv
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Resume, AnalysisReport
from .serializers import ResumeSerializer, AnalysisReportSerializer
import google.generativeai as genai
import pdfplumber
from docx import Document

# Load .env
load_dotenv(os.path.join(settings.BASE_DIR, ".env"))
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY not set in .env")
genai.configure(api_key=api_key)

# --- Text extraction ---
def extract_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("PDF extraction error:", e)
    return text

def extract_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print("DOCX extraction error:", e)
    return text

# --- Gemini resume analysis ---
def analyze_resume(resume_text: str) -> dict:
    """
    Analyze resume:
    - overall_score: 0-100
    - ats_score: 0-100
    - improvement_suggestions by section
    """
    prompt = f"""
Analyze this resume and return ONLY JSON:

1. Give overall_score (0-100) based on clarity, completeness, impact.
2. Give ats_score (0-100) based on ATS readability, keyword usage, and formatting.
3. Give improvement suggestions for each section: skills, experience, education, summary.

Resume Text:
{resume_text}

Return JSON exactly as:
{{
  "overall_score": 0,
  "ats_score": 0,
  "improvement_suggestions": {{
    "skills": [],
    "experience": [],
    "education": [],
    "summary": []
  }}
}}
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        result_json = json.loads(response.text)
    except:
        result_json = {
            "overall_score": 0,
            "ats_score": 0,
            "improvement_suggestions": {
                "skills": [],
                "experience": [],
                "education": [],
                "summary": []
            },
            "raw_text": response.text
        }

    # Ensure keys exist
    result_json.setdefault("overall_score", 0)
    result_json.setdefault("ats_score", 0)
    result_json.setdefault("improvement_suggestions", {
        "skills": [],
        "experience": [],
        "education": [],
        "summary": []
    })

    return result_json

# --- API Views ---
class UploadResumeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        resume = Resume(file=file_obj)
        resume.save()

        file_name = resume.file.name.lower()
        if file_name.endswith('.pdf'):
            text = extract_pdf(resume.file.path)
        elif file_name.endswith('.docx'):
            text = extract_docx(resume.file.path)
        else:
            text = ""

        resume.text = text
        resume.save()
        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)

class AnalyzeResumeView(APIView):
    def post(self, request, format=None):
        resume_id = request.data.get("resume_id")
        if not resume_id:
            return Response({"detail": "resume_id required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resume = Resume.objects.get(pk=resume_id)
        except Resume.DoesNotExist:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        report = analyze_resume(resume.text)
        analysis = AnalysisReport(resume=resume, report_json=report)
        analysis.save()
        return Response(report, status=status.HTTP_201_CREATED)
