from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path(
        "delete/<int:notification_id>/",
        views.delete_notification,
        name="delete",
    ),
    path("mark_as_read/<int:notification_id>/", views.mark_as_read, name="as_read"),
]
