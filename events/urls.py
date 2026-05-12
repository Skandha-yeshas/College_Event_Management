from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('register/', views.register_participant, name='register_participant'),
    path('add/', views.add_event, name='add_event'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('participant-login/', views.participant_login, name='participant_login'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('participant-logout/', views.participant_logout, name='participant_logout'),
    path('export-excel/<int:event_id>/', views.export_event_excel, name='export_event_excel'),
]