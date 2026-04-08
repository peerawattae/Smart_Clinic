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
