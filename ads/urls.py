from django.urls import path
from .views import AdsListView, AdsCreateView, AdsUpdateView, AdsDeleteView

app_name = "ads"

urlpatterns = [
    path("", AdsListView.as_view(), name="list"),
    path("create/", AdsCreateView.as_view(), name="create"),
    path("<pk>/update/", AdsUpdateView.as_view(), name="update"),
    path("<pk>/delete/", AdsDeleteView.as_view(), name="delete"),
]
