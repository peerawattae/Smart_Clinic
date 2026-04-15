from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from ..models import User, Notification
from ..forms import StaffEditForm

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
def all_patients(request):
    patients = User.objects.filter(role=User.Role.PATIENT).prefetch_related(
        'patient_profile', 
        'medical_records',
        'patient_appointments'
    ).order_by('first_name')
    return render(request, 'users/all_patients.html', {
        'patients': patients
    })

@staff_member_required
def approve_doctor(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id, role=User.Role.DOCTOR)
        action = request.POST.get('action')
        
        if action == 'approve':
            user.is_active = True
            user.save()
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
