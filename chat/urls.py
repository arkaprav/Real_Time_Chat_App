from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/',views.create_room, name='create-room'),
    path('chat/<slug:room_slug>/',views.chatPage, name='chat')
]
