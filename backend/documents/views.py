from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Application, Document
from .serializers import DocumentSerializer, ApplicationStatusWithPushbackSerializer

# Return current user's application info
class ApplicationStatusView(generics.RetrieveAPIView):
    serializer_class = ApplicationStatusWithPushbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        app, _ = Application.objects.get_or_create(user=self.request.user)
        return app


# Handles initial upload of Certificate of Incorporation.
class UploadDocumentView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        application, _ = Application.objects.get_or_create(user=self.request.user)
        serializer.save(application=application)


# Allows re-upload of Certificate only if the status is PUSHBACK
class ReuploadDocumentView(generics.UpdateAPIView):

    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(application__user=self.request.user)

    def patch(self, request, *args, **kwargs):
        document = self.get_object()

        # Permission check
        if document.application.user != request.user:
            return Response({"detail": "Not allowed."}, status=403)

        # Business logic check
        if document.application.status != "PUSHBACK":
            return Response({"detail": "Document can only be re-uploaded when application is in PUSHBACK."}, status=400)
        
        # update - reset status of application - we keep status document previously
        document.file = request.data.get("file", document.file)
        document.application.status = "PENDING"
        document.application.reason = ""
        document.application.save()
        document.save()


        return Response(DocumentSerializer(document).data)
