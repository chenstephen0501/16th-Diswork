from django.urls import path
from .views import (
    BoardIndexView,
    BoardNewView,
    BoardDetailView,
    BoardUpdateView,
    BoardDeleteView,
)
from . import views

app_name = "boards"

urlpatterns = [
    path("", BoardIndexView.as_view(), name="list"),
    path("new/", BoardNewView.as_view(), name="new"),
    path("<int:pk>", BoardDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", BoardUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", BoardDeleteView.as_view(), name="delete"),
    path("add/", views.create, name="add"),
]
