from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AnalysisReport(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='reports')
    report_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
