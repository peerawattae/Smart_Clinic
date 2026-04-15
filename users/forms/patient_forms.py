from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientProfileForm(forms.ModelForm):
    blood_type = forms.ChoiceField(choices=[('', 'Select Blood Type')] + [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], required=False)
    allergies = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    emergency_contact_name = forms.CharField(max_length=150, required=False, label="Emergency Contact Name")
    emergency_contact_phone = forms.CharField(max_length=20, required=False, label="Emergency Contact Phone")
    insurance_provider = forms.CharField(max_length=100, required=False)
    insurance_id = forms.CharField(max_length=50, required=False, label="Insurance ID")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..models import PatientProfile
        if self.instance and self.instance.id and self.instance.role == 'patient':
            try:
                profile = self.instance.patient_profile
                self.fields['blood_type'].initial = profile.blood_type
                self.fields['allergies'].initial = profile.allergies
                self.fields['emergency_contact_name'].initial = profile.emergency_contact_name
                self.fields['emergency_contact_phone'].initial = profile.emergency_contact_phone
                self.fields['insurance_provider'].initial = profile.insurance_provider
                self.fields['insurance_id'].initial = profile.insurance_id
            except:
                pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        from ..models import PatientProfile
        if user.role == 'patient':
            profile, created = PatientProfile.objects.get_or_create(user=user)
            profile.blood_type = self.cleaned_data.get('blood_type')
            profile.allergies = self.cleaned_data.get('allergies')
            profile.emergency_contact_name = self.cleaned_data.get('emergency_contact_name')
            profile.emergency_contact_phone = self.cleaned_data.get('emergency_contact_phone')
            profile.insurance_provider = self.cleaned_data.get('insurance_provider')
            profile.insurance_id = self.cleaned_data.get('insurance_id')
            profile.save()
        return user
