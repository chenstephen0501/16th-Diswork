from django.urls import path, include
from .views import (
    ArticleIndexView,
    NewView,
    DeleteView,
    ShowView,
    add_like,
    remove_like,
)
from comments.views import CommentCreateView
from . import views

app_name = "articles"

urlpatterns = [
    path("", ArticleIndexView.as_view(), name="index"),
    path("add/", views.create, name="add"),
    path("new/", NewView.as_view(), name="new"),
    path("<pk>/edit/", views.edit, name="edit"),
    path("<pk>/delete/", DeleteView.as_view(), name="delete"),
    path("<pk>/comment/", CommentCreateView.as_view(), name="comment"),
    path("<pk>/", ShowView.as_view(), name="show"),
    path("<pk>/add_like", add_like, name="add_like"),
    path("<pk>/remove_like", remove_like, name="remove_like"),
]
