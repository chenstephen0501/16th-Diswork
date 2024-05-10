from django.urls import path
from . import views


app_name = "chats"

urlpatterns = [
    path('', views.chat_view_home, name = "home"),
    path('new', views.chat_view_new, name = "new"),
    path('add', views.chat_view_create, name = "add"),
    path('chats/<int:id>/', views.chat_view_show, name='show'),
]
