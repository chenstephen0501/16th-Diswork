from django.urls import path
from .views import CommentListView, add_like, remove_like, CommentDeleteView

app_name = "comments"

urlpatterns = [
    path("<pk>/delete/", CommentDeleteView.as_view(), name="delete"),
    path("<pk>/add_like", add_like, name="add_like"),
    path("<pk>/remove_like", remove_like, name="remove_like"),
    path("<pk>/", CommentListView.as_view(), name="list"),
]
