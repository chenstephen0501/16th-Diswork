from django.urls import path
from .views import (
    BoardIndexView,
    BoardNewView,
    BoardDetailView,
    CategoryUpdateView,
    BoardDeleteView,
)
from . import views

app_name = "boards"

urlpatterns = [
    path("", BoardIndexView.as_view(), name="list"),
    path("new/", BoardNewView.as_view(), name="new"),
    path("<int:pk>", BoardDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", BoardDeleteView.as_view(), name="delete"),
    path("add/", views.create, name="add"),
    path("upload_picture/", views.upload_picture, name="upload_picture"),
]
