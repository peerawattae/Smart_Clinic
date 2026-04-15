from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, StaffEditForm
from .models import Notification, User, DoctorProfile


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


@staff_member_required
def admin_dashboard(request):
    pending_doctors = User.objects.filter(role=User.Role.DOCTOR, is_active=False)
    active_staff = User.objects.filter(
        role__in=[User.Role.DOCTOR, User.Role.NURSE, User.Role.STAFF, User.Role.ADMIN],
        is_active=True
    ).exclude(id=request.user.id).order_by('role', 'first_name')
    
    return render(request, 'users/admin_dashboard.html', {
        'pending_doctors': pending_doctors,
        'active_staff': active_staff
    })

@staff_member_required
def approve_doctor(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id, role=User.Role.DOCTOR)
        action = request.POST.get('action')
        
        if action == 'approve':
            user.is_active = True
            user.save()
            # Send notification to the doctor?
            Notification.objects.create(
                user=user,
                title="Account Approved",
                message="Your doctor account has been approved. You can now log in and manage your schedule."
            )
        elif action == 'reject':
            user.delete()
            
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@staff_member_required
def toggle_staff_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_staff or user.role in [User.Role.DOCTOR, User.Role.NURSE, User.Role.STAFF, User.Role.ADMIN]:
            user.is_active = not user.is_active
            user.save()
            
            action = "activated" if user.is_active else "deactivated"
            Notification.objects.create(
                user=user,
                title=f"Account {action.capitalize()}",
                message=f"Your account has been {action} by an administrator."
            )
            
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@staff_member_required
def edit_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StaffEditForm(instance=user)
    
    return render(request, 'users/edit_staff.html', {
        'form': form,
        'staff': user
    })


