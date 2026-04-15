from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import MedicalRecord, MedicalRecordAccessRequest, Prescription
from .forms import MedicalRecordForm, PrescriptionFormSet
from appointments.models import Appointment
from users.models import Notification, User

class MedicalRecordCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'records/medical_record_form.html'

    def test_func(self):
        return self.request.user.role == 'doctor' or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = get_object_or_404(Appointment, pk=self.kwargs.get('appointment_id'))
        context['appointment'] = appointment
        if self.request.POST:
            context['prescriptions'] = PrescriptionFormSet(self.request.POST)
        else:
            context['prescriptions'] = PrescriptionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        prescriptions = context['prescriptions']
        appointment = context['appointment']
        
        form.instance.doctor = self.request.user
        form.instance.patient = appointment.patient
        form.instance.appointment = appointment
        
        if prescriptions.is_valid():
            self.object = form.save()
            prescriptions.instance = self.object
            prescriptions.save()
            
            appointment.status = 'completed'
            appointment.save()
            
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('appointments:appointment_detail', kwargs={'pk': self.kwargs.get('appointment_id')})

class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'records/medical_record_detail.html'
    context_object_name = 'record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record = self.get_object()
        user = self.request.user
        
        # Check access status
        has_access = False
        if user == record.doctor or user.is_superuser or user.role == 'admin':
            has_access = True
        elif user == record.patient:
            # Check for approved access request
            access_request = MedicalRecordAccessRequest.objects.filter(record=record, patient=user, status='approved').first()
            if access_request:
                has_access = True
            else:
                context['pending_request'] = MedicalRecordAccessRequest.objects.filter(record=record, patient=user, status='pending').exists()
        
        context['has_access'] = has_access
        context['prescriptions'] = record.prescriptions.all()
        return context

def request_medical_record_access(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(MedicalRecord, id=record_id)
        if request.user != record.patient:
            messages.error(request, "You can only request access to your own records.")
            return redirect('appointments:appointment_list')
        
        access_request, created = MedicalRecordAccessRequest.objects.get_or_create(
            record=record, 
            patient=request.user
        )
        
        if created:
            # Notify the doctor
            Notification.objects.create(
                user=record.doctor,
                title="New Case Access Request",
                message=f"Patient {request.user.get_full_name()} has requested access to the full medical record for the visit on {record.created_at.date()}.",
                link=reverse('records:record_detail', kwargs={'pk': record.id})
            )
            messages.success(request, "Access request sent to Dr. " + record.doctor.get_full_name())
        else:
            messages.info(request, "You already have a " + access_request.status + " request for this record.")
            
        return redirect('records:record_detail', pk=record_id)
    return redirect('appointments:appointment_list')

def approve_medical_record_access(request, request_id):
    access_request = get_object_or_404(MedicalRecordAccessRequest, id=request_id)
    
    # Only the authoring doctor or admin can approve
    if request.user != access_request.record.doctor and not request.user.role == 'admin':
        messages.error(request, "Unauthorized.")
        return redirect('home')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            access_request.status = 'approved'
            access_request.approval_date = timezone.now()
            access_request.save()
            
            # Notify patient
            Notification.objects.create(
                user=access_request.patient,
                title="Medical Record Access Approved",
                message=f"Dr. {request.user.get_full_name()} has approved your request to view the full medical record from {access_request.record.created_at.date()}.",
                link=reverse('records:record_detail', kwargs={'pk': access_request.record.id})
            )
            messages.success(request, "Request approved.")
        elif action == 'reject':
            access_request.status = 'rejected'
            access_request.save()
            messages.info(request, "Request rejected.")
            
        return redirect('records:record_detail', pk=access_request.record.id)
    return redirect('home')
