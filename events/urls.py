from django.urls import path
from . import views
from .views import CalendarView, NewView, EventListView

app_name = "events"

urlpatterns = [
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("list/", EventListView.as_view(), name="list"),
    path("all_events/", views.all_events, name="all_events"),
    path("new", NewView.as_view(), name="new"),
    path("add/", views.create, name="add"),
    path("<int:id>/edit/", views.edit, name="edit"),
]
