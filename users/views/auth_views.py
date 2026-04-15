from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from ..forms import CustomUserCreationForm
from ..models import Notification, User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.role = role
            
            if role == 'doctor':
                user.is_active = False # Pending admin approval
                user.save()
                
                # Save doctor profile info
                profile = user.doctor_profile
                profile.specialization = form.cleaned_data.get('specialization')
                profile.license_number = form.cleaned_data.get('license_number')
                profile.save()
                
                # Notify all admins
                admins = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True) | Q(role=User.Role.ADMIN))
                for admin in admins:
                    Notification.objects.create(
                        user=admin,
                        title="New Doctor Pending Approval",
                        message=f"Dr. {user.get_full_name()} has registered and is waiting for approval."
                    )
                
                return render(request, 'users/login.html', {
                    'form': AuthenticationForm(),
                    'message': 'Doctor account created! Please wait for an Admin to approve your account before signing in.'
                })
            else:
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

def logout_view(request):
    logout(request)
    return redirect('home')
