from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('register/', views.register_participant, name='register_participant'),
    path('add/', views.add_event, name='add_event'),
]