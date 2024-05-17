from django.urls import path
from . import views
from .views import NewView

app_name = "events"

urlpatterns = [
    path("events/", views.calendar_events, name="calendar"),
    path("all_events/", views.all_events, name="all_events"),
    path("new", NewView.as_view(), name="new"),
    path("add/", views.create_my_event, name="add_event"),
    path("edit/", views.edit, name="edit_event"),
]
