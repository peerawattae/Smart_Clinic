from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor')
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='patient', widget=forms.RadioSelect)
    
    # Doctor specific fields
    specialization = forms.CharField(max_length=100, required=False)
    license_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'doctor':
            if not cleaned_data.get('specialization'):
                self.add_error('specialization', 'Specialization is required for doctors.')
            if not cleaned_data.get('license_number'):
                self.add_error('license_number', 'License number is required for doctors.')
        return cleaned_data

class StaffEditForm(forms.ModelForm):
    specialization = forms.CharField(max_length=100, required=False)
    license_number = forms.CharField(max_length=50, required=False)
    years_of_experience = forms.IntegerField(min_value=0, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import DoctorProfile
        if self.instance and self.instance.id and self.instance.role == 'doctor':
            try:
                profile = self.instance.doctor_profile
                self.fields['specialization'].initial = profile.specialization
                self.fields['license_number'].initial = profile.license_number
                self.fields['years_of_experience'].initial = profile.years_of_experience
                self.fields['bio'].initial = profile.bio
            except:
                pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        from .models import DoctorProfile
        if user.role == 'doctor':
            profile, created = DoctorProfile.objects.get_or_create(user=user)
            profile.specialization = self.cleaned_data.get('specialization')
            profile.license_number = self.cleaned_data.get('license_number')
            profile.years_of_experience = self.cleaned_data.get('years_of_experience') or 0
            profile.bio = self.cleaned_data.get('bio')
            profile.save()
        return user

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
        from .models import PatientProfile
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
        from .models import PatientProfile
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
