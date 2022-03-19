from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('room/',views.room,name='room'),
    path('private-room/',views.privateRoom,name='privateroom'),
]