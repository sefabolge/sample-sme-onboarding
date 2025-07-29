# core/serializers.py

from rest_framework import serializers
from core.models import User
from documents.models import Application, Document

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    certificate = serializers.FileField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "full_name", "password", "certificate"]

    def create(self, validated_data):
        certificate = validated_data.pop("certificate")
        password = validated_data.pop("password")

        # Create user and hash password
        user = User.objects.create_user(**validated_data, password=password)

        # Create application
        application = Application.objects.create(user=user)

        # Save certificate - # COI = Certificate of Incorporation
        Document.objects.create(application=application, file=certificate,  doc_type="COI")  

        return user
