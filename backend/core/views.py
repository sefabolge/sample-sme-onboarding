from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.models import User
from .serializers import UserSignupSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]
