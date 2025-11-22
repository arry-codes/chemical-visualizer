from django.urls import path
from .views import FileUploadView, HistoryView, SummaryView, PDFReportView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('history/', HistoryView.as_view(), name='upload-history'),
    path('summary/<int:upload_id>/', SummaryView.as_view(), name='upload-summary'),
    path('pdf/<int:upload_id>/', PDFReportView.as_view(), name='pdf-report'),
]
