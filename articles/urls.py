from django.urls import path
from .views import (
    ArticleIndexView,
    ArticleUpdateView,
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
    path("category/<int:category_id>/", ArticleIndexView.as_view(), name="index"),
    path("category/<int:category_id>/new/", NewView.as_view(), name="new"),
    path("category/<int:category_id>/add/", views.create, name="add"),
    path("add/", views.create, name="add"),
    path("new/", NewView.as_view(), name="new"),
    path("<pk>/edit/", ArticleUpdateView.as_view(), name="edit"),
    path("<pk>/delete/", DeleteView.as_view(), name="delete"),
    path("<pk>/comment/", CommentCreateView.as_view(), name="comment"),
    path("<pk>/add_like", add_like, name="add_like"),
    path("<pk>/remove_like", remove_like, name="remove_like"),
    path("<pk>/", ShowView.as_view(), name="show"),
]
