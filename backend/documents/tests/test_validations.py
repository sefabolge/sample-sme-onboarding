# documents/tests/test_validations.py
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.serializers import DocumentSerializer
from documents.models import Application

@pytest.mark.django_db
def test_large_file_upload_rejected(user, settings):
    settings.MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
    Application.objects.create(user=user)

    large_file = SimpleUploadedFile(
        "large_test.pdf", b"A" * (11 * 1024 * 1024), content_type="application/pdf"
    )
    data = {"doc_type": "COI", "file": large_file}
    context = {"request": type("Request", (), {"user": user})}
    serializer = DocumentSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert "file" in serializer.errors
