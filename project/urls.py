from django.contrib import admin
from django.urls import path, include
from .views import AboutUsView, index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="root"),
    path("aboutus/", AboutUsView.as_view(), name="aboutus"),
    path("members/", include("members.urls")),
    path("friends/", include("friends.urls")),
    path("events/", include("events.urls")),
    path("news/", include("news.urls")),
    path("chat/", include("chats.urls")),
    path("tasks/", include("tasks.urls")),
    path("boards/", include("boards.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
    path("articles/", include("articles.urls")),
    path("paies/", include("paies.urls")),
    path("ads/", include("ads.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
