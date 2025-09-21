from rest_framework import serializers
from .models import Resume, AnalysisReport

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'text', 'uploaded_at']

class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ['id', 'resume', 'report_json', 'created_at']
