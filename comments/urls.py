from django.urls import path
from .views import CommentCreateView, CommentDeleteView, CommentListView

app_name = "comments"

urlpatterns = [
    path("<id>/", CommentListView.as_view(), name="comment_area"),
    path("<id>/add/", CommentCreateView.as_view(), name="comment_add"),
    path("<pk>/delete/", CommentDeleteView.as_view(), name="delete"),
]