from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("create/", views.create, name="create"),
    path("<pk>/edit", views.edit, name="edit"),
    path("<pk>/delete", views.delete, name="delete"),
    path("<pk>", views.show, name="show"),
]
