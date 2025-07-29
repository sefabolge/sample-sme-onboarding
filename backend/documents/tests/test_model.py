# documents/tests/test_model.py
import pytest
from documents.models import Application, Document
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_application_str():
    user = User.objects.create_user(username="testuser", full_name="Test User", password="pass1234")
    app = Application.objects.create(user=user)
    assert str(app) == f"Application for {user.username} [{app.status}]"

@pytest.mark.django_db
def test_document_str():
    user = User.objects.create_user(username="docuser", full_name="Doc User", password="pass1234")
    app = Application.objects.create(user=user)
    doc = Document.objects.create(application=app, doc_type="COI", file="dummy.pdf")
    assert str(doc) == f"{doc.doc_type} for {user.username}"
