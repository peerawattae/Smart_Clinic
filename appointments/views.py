from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Appointment

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        # Patient sees their own appointments
        if hasattr(user, 'role') and user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        # Doctor sees their own appointments
        elif hasattr(user, 'role') and user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        # Admins or Staff might see all
        return Appointment.objects.all()

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif hasattr(user, 'role') and user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        return Appointment.objects.all()

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'appointments/appointment_form.html'
    fields = ['doctor', 'date', 'time_slot', 'end_time', 'reason']
    success_url = reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        # Automatically set the current logged in user as the patient
        form.instance.patient = self.request.user
        return super().form_valid(form)
