from django.urls import path
from . import views


app_name = "chats"

urlpatterns = [
    path("", views.chat_home, name = "home"),
    path("new", views.chat_new, name = "new"),
    path("add", views.chat_create, name = "add"),
    path("chats/<int:id>/", views.chat_show, name="show"),
    path("private_messages/", views.private_message_home, name="index"),
    path("<str:room_name>/", views.private_message_room, name='private_message_room'),
]
