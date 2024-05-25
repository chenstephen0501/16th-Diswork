from django.urls import path
from . import views
from .views import CalendarView, NewView

app_name = "events"

urlpatterns = [
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("all_events/", views.all_events, name="all_events"),
    path("new", NewView.as_view(), name="new"),
    path("add/", views.create, name="add"),
    path("edit/", views.edit, name="edit"),
]
