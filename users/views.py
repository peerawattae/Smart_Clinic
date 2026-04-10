from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Notification


def home_view(request):
    # if request.user.is_authenticated:
    #     # Redirect based on user role
    #     if request.user.is_superuser or request.user.username == 'admin':
    #         return redirect('admin:index')
    #     return redirect('appointments:appointment_list')
    
    # Render the beautiful landing page for everyone
    return render(request, 'users/home.html')

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

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'users/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.user.notifications.filter(is_read=False).update(is_read=True)
        return context

@login_required
def delete_notification(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        request.user.notifications.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


