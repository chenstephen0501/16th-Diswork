from django.urls import path
from . import views
from .views import CommentListView

app_name = "comments"

urlpatterns = [
    path("<pk>/", CommentListView.as_view(), name="list"),
    path("<pk>/delete/", views.delete, name="delete"),
]
