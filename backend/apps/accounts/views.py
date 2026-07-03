from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model

from .permissions import IsAdminUser
from .serializers import RegisterSerializer, UserSerializer, AdminUserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class AdminUserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all().order_by("-date_joined")

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            kwargs.setdefault("data", self.request.data)
            data = dict(kwargs.get("data") or {})
            if "password_confirm" not in data and "password" in data:
                data["password_confirm"] = data["password"]
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)


class AdminUserDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id == request.user.id:
            return Response(
                {"detail": "You cannot delete your own admin account."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
