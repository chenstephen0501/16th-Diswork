from django.contrib import admin
from django.urls import path, include
from .views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("members/", include("members.urls")),
    path("friends/", include("friends.urls")),
    path("calendar/", include("events.urls")),
    path("news/", include("news_app.urls")),
    path("chat/", include("chats.urls")),
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
]
