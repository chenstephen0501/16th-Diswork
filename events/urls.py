from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("events/", views.calendar_events, name="calendar"),
]
