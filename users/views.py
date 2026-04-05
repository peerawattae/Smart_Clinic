from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm

def home_view(request):
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.is_superuser or request.user.username == 'admin':
            return redirect('admin:index')
        return redirect('appointments:appointment_list')
    
    # If not authenticated, render the beautiful landing page
    return render(request, 'users/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Patient role by default, although models default to it anyway
            user.role = 'patient'
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})
