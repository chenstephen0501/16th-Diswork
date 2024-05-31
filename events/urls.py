from django.urls import path
from . import views
from .views import (
    CalendarView,
    NewView,
    EventListView,
    EventUpdateView,
    EventDeleteView,
)

app_name = "events"

urlpatterns = [
    path("category/<int:category_id>/calendar/", CalendarView.as_view(), name="calendar"),
    path("category/<int:category_id>/list/", EventListView.as_view(), name="list"),
    path("category/<int:category_id>/all_events/", views.all_events, name="all_events"),
    path("category/<int:category_id>/new", NewView.as_view(), name="new"),
    path("category/<int:category_id>/add/", views.create, name="add"),
    path("category/<int:category_id>/<int:pk>/edit/", EventUpdateView.as_view(), name="edit"),
    path("category/<int:category_id>/<int:pk>/delete/", EventDeleteView.as_view(), name="delete"),
]
