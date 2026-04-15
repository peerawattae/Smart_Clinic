from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import PatientProfileForm

def home_view(request):
    return render(request, 'users/home.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PatientProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {
        'form': form
    })
