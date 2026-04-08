from django import forms
from django.contrib.auth import get_user_model
from .models import Appointment

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    TIME_CHOICES = [
        ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
        ('13:00', '01:00 PM'), ('13:30', '01:30 PM'),
        ('14:00', '02:00 PM'), ('14:30', '02:30 PM'),
        ('15:00', '03:00 PM'), ('15:30', '03:30 PM'),
        ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
    ]

    time_slot = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'glass-input'}))
    end_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'glass-input'}))

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time_slot', 'end_time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'glass-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.role == 'doctor':
                # Doctors see a list of patients
                self.fields['patient'].queryset = User.objects.filter(role='patient')
                self.fields['patient'].label = "Select Patient"
                self.fields['patient'].empty_label = "Choose a patient..."
                
                # Auto-select the logged-in doctor and hide field
                self.fields['doctor'].initial = user
                self.fields['doctor'].widget = forms.HiddenInput()
                self.fields['doctor'].required = False
                
            elif user.role == 'patient':
                # Auto-select the logged-in patient and hide field
                self.fields['patient'].initial = user
                self.fields['patient'].widget = forms.HiddenInput()
                self.fields['patient'].required = False
                
                # Patients choose from doctors
                self.fields['doctor'].queryset = User.objects.filter(role='doctor')
                self.fields['doctor'].label = "Select Doctor"
                self.fields['doctor'].empty_label = "Choose a specialist..."

        # Apply consistent styling
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({'class': 'glass-input'})

