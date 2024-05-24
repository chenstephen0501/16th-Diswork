from django.urls import path, include
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleIndexView.as_view(), name="index"),
    path("add", views.create, name="add"),
    path("new", views.NewView.as_view(), name="new"),
    path("<id>/edit", views.edit, name="edit"),
    # path("<id>/delete", views.delete, name="delete"),
    path("<pk>/delete", views.DeleteView.as_view(), name="delete"),
    path("<pk>", views.ShowView.as_view(), name="show"),
]
