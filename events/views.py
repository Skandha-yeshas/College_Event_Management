from django.shortcuts import render, redirect
from .models import Event, Participant
from django import forms
from .forms import EventForm, ParticipantForm

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
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})