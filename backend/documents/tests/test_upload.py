import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.models import Application, Document

@pytest.mark.django_db
def test_valid_document_upload(user):
    app = Application.objects.create(user=user)

    file = SimpleUploadedFile("test.pdf", b"dummy data", content_type="application/pdf")
    doc = Document.objects.create(
        application=app,
        doc_type="COI",
        file=file
    )

    assert doc.status == "PENDING"
    assert doc.application == app
