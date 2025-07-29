from django.db import models
from django.conf import settings
from .utils import user_document_path

class Application(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("PUSHBACK", "Pushback"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    reason = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Application for {self.user.username} [{self.status}]"


class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ("COI", "Certificate of Incorporation"),
        ("ID", "Identification"),
        ("PROOF", "Proof of Address"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("PUSHBACK", "Pushback"),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default="COI")
    file = models.FileField(upload_to=user_document_path)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    pushback_reason = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} for {self.application.user.username}"
