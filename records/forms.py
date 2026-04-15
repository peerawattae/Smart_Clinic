from django import forms
from .models import MedicalRecord, Prescription, VitalSign

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'symptoms', 'treatment', 'notes', 'follow_up_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 2, 'class': 'glass-input', 'placeholder': 'Enter diagnosis...'}),
            'symptoms': forms.Textarea(attrs={'rows': 2, 'class': 'glass-input', 'placeholder': 'Describe symptoms...'}),
            'treatment': forms.Textarea(attrs={'rows': 2, 'class': 'glass-input', 'placeholder': 'Outline treatment plan...'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'glass-input', 'placeholder': 'Additional notes...'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'glass-input'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'glass-input'}),
            'dosage': forms.TextInput(attrs={'class': 'glass-input'}),
            'frequency': forms.TextInput(attrs={'class': 'glass-input'}),
            'duration': forms.TextInput(attrs={'class': 'glass-input'}),
            'instructions': forms.Textarea(attrs={'rows': 2, 'class': 'glass-input'}),
        }

class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = ['temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'respiratory_rate', 'weight', 'height']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'glass-input', 'step': '0.1'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'glass-input'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'glass-input'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'glass-input'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'glass-input'}),
            'weight': forms.NumberInput(attrs={'class': 'glass-input', 'step': '0.01'}),
            'height': forms.NumberInput(attrs={'class': 'glass-input', 'step': '0.01'}),
        }

from django.forms import inlineformset_factory

PrescriptionFormSet = inlineformset_factory(
    MedicalRecord, 
    Prescription, 
    form=PrescriptionForm, 
    extra=1, 
    can_delete=True
)
