from django.urls import path
from .views import ApplicationStatusView, UploadDocumentView, ReuploadDocumentView

urlpatterns = [
    path("application/status/", ApplicationStatusView.as_view(), name="application-status"),
    path("documents/upload/", UploadDocumentView.as_view(), name="document-upload"),
    path("documents/<int:pk>/reupload/", ReuploadDocumentView.as_view(), name="document-reupload"),
]
