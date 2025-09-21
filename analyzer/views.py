from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Resume, AnalysisReport
from .serializers import ResumeSerializer, AnalysisReportSerializer
from .gemini_client import analyze_resume

# File parsing imports
import pdfplumber
from docx import Document
import json

# --- File extraction helpers ---
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

# --- Upload Resume ---
class UploadResumeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        resume = Resume(file=file_obj)
        resume.save()

        # Extract text based on file type
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

# --- Analyze Resume ---
class AnalyzeResumeView(APIView):
    def post(self, request, format=None):
        resume_id = request.data.get('resume_id')
        if not resume_id:
            return Response({"detail": "resume_id required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            resume = Resume.objects.get(pk=resume_id)
        except Resume.DoesNotExist:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            report = analyze_resume(resume.text)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Parse raw_text if returned by Gemini
        raw_text = report.get("raw_text")
        if raw_text:
            try:
                parsed_json = json.loads(raw_text.strip("```json\n").strip("```"))
            except json.JSONDecodeError:
                parsed_json = {"raw_text": raw_text}
        else:
            parsed_json = report

        # --- Ensure clean structure ---
        # Overall score (0-100)
        if "overall_score" not in parsed_json or not isinstance(parsed_json["overall_score"], int):
            parsed_json["overall_score"] = 0

        # ATS friendliness score (0-100)
        if "ats_score" not in parsed_json or not isinstance(parsed_json["ats_score"], int):
            parsed_json["ats_score"] = 0

        # Section-wise improvement suggestions
        parsed_json.setdefault("improvement_suggestions", {
            "skills": [],
            "experience": [],
            "education": [],
            "summary": []
        })

        # Save to DB
        analysis = AnalysisReport(resume=resume, report_json=parsed_json)
        analysis.save()

        # Return parsed_json directly
        return Response(parsed_json, status=status.HTTP_201_CREATED)
