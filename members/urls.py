from django.urls import path
from .views import LoginView, LogoutView, RegisterView, MemberUpdateView
from . import views

app_name = "members"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("edit/", MemberUpdateView.as_view(), name="edit"),
    # 註冊mail
    path("activate/<uidb64>/<token>/", views.activate, name="activate"), 
]
