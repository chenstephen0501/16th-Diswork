from django.urls import path
from .views import CommentDeleteView, CommentListView

app_name = "comments"

urlpatterns = [
    path("<pk>/", CommentListView.as_view(), name="list"),
    path("<pk>/delete/", CommentDeleteView.as_view(), name="delete"),
]
