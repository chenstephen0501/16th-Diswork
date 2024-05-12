from django.urls import path
from . import views
from .views import NewView

app_name = "events"

urlpatterns = [
    path("events/", views.calendar_events, name="calendar"),
    path("my_event/", views.my_event_calendar, name="my_calendar"),
    path("new", NewView.as_view(), name="new"),
    path("add/", views.create_my_event, name="add_event"),
    path("edit/", views.edit, name="edit_event"),
]
