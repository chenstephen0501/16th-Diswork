from django.urls import path
from .views import NewsSearchView
from . import views

app_name = "news"

urlpatterns = [
    path("news/", NewsSearchView.as_view(), name="search"),
    path("", views.news_json, name="news_json"),
]
