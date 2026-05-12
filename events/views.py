from django.shortcuts import render, redirect
from .models import Event, Participant
import csv
import openpyxl
from django.http import HttpResponse
from django import forms
from datetime import date
from .forms import EventForm, ParticipantForm
from django.core.mail import send_mail
from django.conf import settings

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'

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
    initial = {}
    event_id = request.GET.get('event_id')
    if event_id:
        initial['event'] = event_id
        
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            
            # Send confirmation email
            event = participant.event
            subject = f"Registration Confirmation: {event.name}"
            message = (
                f"Hi {participant.name},\n\n"
                f"You have successfully registered for '{event.name}'.\n\n"
                f"Event Details:\n"
                f"Date: {event.date}\n"
                f"Location: {event.location}\n"
                f"Description: {event.description}\n\n"
                f"Thank you!\nCollege Events Team"
            )
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [participant.email],
                    fail_silently=True,
                )
            except Exception:
                pass
                
            return redirect('home')
    else:
        form = ParticipantForm(initial=initial)
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

def delete_event(request, event_id):
    if not request.session.get('is_custom_admin'):
        return redirect('admin_login')
        
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
        except Event.DoesNotExist:
            pass
    return redirect('admin_dashboard')

def edit_event(request, event_id):
    if not request.session.get('is_custom_admin'):
        return redirect('admin_login')
        
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm(instance=event)
        
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

def export_event_excel(request, event_id):
    if not request.session.get('is_custom_admin'):
        return redirect('admin_login')
        
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return redirect('admin_dashboard')
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_participants.xlsx"'
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Participants"
    
    headers = ['Name', 'Email', 'Phone', 'DOB']
    sheet.append(headers)
    
    participants = event.participant_set.all()
    for p in participants:
        dob_str = p.dob.strftime('%Y-%m-%d') if p.dob else ''
        sheet.append([p.name, p.email, p.phone, dob_str])
        
    workbook.save(response)
    return response

def participant_login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        
        # Check if participant exists
        if Participant.objects.filter(name=name, email=email).exists():
            request.session['participant_name'] = name
            request.session['participant_email'] = email
            return redirect('participant_dashboard')
        else:
            return render(request, 'events/participant_login.html', {'error': 'Invalid username or email'})
    
    return render(request, 'events/participant_login.html')

def participant_logout(request):
    if 'participant_name' in request.session:
        del request.session['participant_name']
    if 'participant_email' in request.session:
        del request.session['participant_email']
    return redirect('home')

def participant_dashboard(request):
    name = request.session.get('participant_name')
    email = request.session.get('participant_email')
    
    if not name or not email:
        return redirect('participant_login')
        
    participants = Participant.objects.filter(name=name, email=email).select_related('event')
    events = [p.event for p in participants]
    
    today = date.today()
    ongoing_events = [e for e in events if e.date >= today]
    completed_events = [e for e in events if e.date < today]
    
    return render(request, 'events/participant_dashboard.html', {
        'ongoing_events': ongoing_events, 
        'completed_events': completed_events,
        'participant_name': name
    })