from django.shortcuts import render, redirect
from .models import Event, Participant
from django import forms
from .forms import EventForm, ParticipantForm

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'

# Participant Registration Form
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'event']

# Home Page
def home(request):
    events = Event.objects.all()  # fetch all events from database
    return render(request, 'events/home.html', {'events': events})
# Event List
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# Register Participant
def register_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ParticipantForm()
    return render(request, 'events/register_participant.html', {'form': form})

def add_event(request):
    if not request.session.get('is_custom_admin'):
        return redirect('admin_login')
        
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

# Custom Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['is_custom_admin'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'events/admin_login.html', {'error': 'Invalid username or password'})
    return render(request, 'events/admin_login.html')

# Custom Admin Logout
def admin_logout(request):
    if 'is_custom_admin' in request.session:
        del request.session['is_custom_admin']
    return redirect('home')

# Custom Admin Dashboard
def admin_dashboard(request):
    if not request.session.get('is_custom_admin'):
        return redirect('admin_login')
    
    events = Event.objects.prefetch_related('participant_set').all()
    return render(request, 'events/admin_dashboard.html', {'events': events})