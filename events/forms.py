from django import forms
from .models import Event
from .models import Participant
from datetime import date

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone', 'dob', 'event']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age <= 18:
                raise forms.ValidationError('Participant must be above 18 years of age.')
        return dob