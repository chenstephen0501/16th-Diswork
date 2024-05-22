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
    path("", BoardIndexView.as_view(), name="board_list"),
    path("new/", BoardNewView.as_view(), name="board_new"),
    path("<int:pk>", BoardDetailView.as_view(), name="board_detail"),
    path("<int:pk>/edit/", CategoryUpdateView.as_view(), name="board_edit"),
    path("<int:pk>/delete", BoardDeleteView.as_view(), name="board_delete"),
    path("add/", views.create, name="board_add"),
]
