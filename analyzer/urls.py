from django.urls import path
from .views import UploadResumeView, AnalyzeResumeView

urlpatterns = [
    path('upload/', UploadResumeView.as_view(), name='upload-resume'),
    path('analyze/', AnalyzeResumeView.as_view(), name='analyze-resume'),
]
