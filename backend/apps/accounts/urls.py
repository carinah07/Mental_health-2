from django.urls import path

from .views import (
    RegisterView,
    MeView,
    LoginView,
    RefreshView,
    AdminUserListCreateView,
    AdminUserDetailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("admin/users/", AdminUserListCreateView.as_view(), name="admin_users"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
]
