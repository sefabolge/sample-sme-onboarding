from rest_framework import serializers
from .models import Application, Document

# --- Document Serializer ---
class DocumentSerializer(serializers.ModelSerializer):
    MAX_FILE_SIZE_MB = 10

    class Meta:
        model = Document
        fields = [
            "id",
            "doc_type",
            "file",
            "status",
            "pushback_reason",
            "uploaded_at"
        ]
        read_only_fields = ["status", "pushback_reason", "uploaded_at"]

    def create(self, validated_data):
        # Associate document with the current user's application
        validated_data["application"] = self.context["request"].user.application
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Allow reupload logic: replace file and reset status if needed
        instance.file = validated_data.get("file", instance.file)
        instance.status = "PENDING"
        instance.pushback_reason = ""
        instance.save()
        return instance

    def validate_file(self, file):
        if file.size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError("File size must be under 10MB.")
        return file

# --- Basic Application Serializer  ---
class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ["id", "status", "reason", "documents", "user"]
        read_only_fields = ["id", "status", "reason", "documents", "user"]


# --- Public-facing dashboard serializer ---
class ApplicationStatusOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "reason"]


# --- Serializer to show a PUSHBACK document (if exists) ---
class PushedBackDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "doc_type", "status", "pushback_reason", "uploaded_at"]


# --- Combined Application Status + Pushback Info for frontend dashboard ---
class ApplicationStatusWithPushbackSerializer(serializers.ModelSerializer):
    pushed_back_document = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ["status", "reason", "pushed_back_document"]

    def get_pushed_back_document(self, obj):
        doc = obj.documents.filter(status="PUSHBACK").first()
        if doc:
            return PushedBackDocumentSerializer(doc).data
        return None
