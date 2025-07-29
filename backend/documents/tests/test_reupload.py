# documents/tests/test_reupload.py
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.models import Application, Document
from documents.serializers import DocumentSerializer

@pytest.mark.django_db
def test_reupload_resets_status(user):
    app = Application.objects.create(user=user)
    file = SimpleUploadedFile("old.pdf", b"old", content_type="application/pdf")

    doc = Document.objects.create(
        application=app,
        doc_type="COI",
        file=file,
        status="PUSHBACK",
        pushback_reason="Blurry"
    )

    new_file = SimpleUploadedFile("new.pdf", b"new", content_type="application/pdf")
    data = {"file": new_file}
    context = {"request": type("Request", (), {"user": user})}

    serializer = DocumentSerializer(instance=doc, data=data, context=context, partial=True)
    assert serializer.is_valid()
    serializer.save()

    doc.refresh_from_db()
    assert doc.status == "PENDING"
    assert doc.pushback_reason == ""
