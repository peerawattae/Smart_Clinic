from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

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
        from ..models import DoctorProfile
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
        from ..models import DoctorProfile
        if user.role == 'doctor':
            profile, created = DoctorProfile.objects.get_or_create(user=user)
            profile.specialization = self.cleaned_data.get('specialization')
            profile.license_number = self.cleaned_data.get('license_number')
            profile.years_of_experience = self.cleaned_data.get('years_of_experience') or 0
            profile.bio = self.cleaned_data.get('bio')
            profile.save()
        return user
