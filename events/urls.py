from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("calendar_events/", views.calendar_events, name="calendar"),
]
