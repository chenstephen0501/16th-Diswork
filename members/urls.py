from django.urls import path
from .views import LoginView, LogoutView, RegisterView, MemberUpdateView, ProfileView
from . import views

app_name = "members"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<pk>", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("edit/<pk>", MemberUpdateView.as_view(), name="edit"),
    # 註冊mail
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
