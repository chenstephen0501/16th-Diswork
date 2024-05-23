from django.urls import path
from . import views
from .views import CommentListView, add_like, remove_like

app_name = "comments"

urlpatterns = [
    path("<pk>/", CommentListView.as_view(), name="list"),
    path("<pk>/delete/", views.delete, name="delete"),
    path("<pk>/add_like", add_like, name="add_like"),
    path("<pk>/remove_like", remove_like, name="remove_like"),
]
