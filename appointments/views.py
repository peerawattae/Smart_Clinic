from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Appointment, DoctorAvailability

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.none()

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        if user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.none()

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'appointments/appointment_form.html'
    fields = ['doctor', 'date', 'time_slot', 'end_time', 'reason']
    success_url = reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)

class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    template_name = 'appointments/appointment_form.html'
    fields = ['status', 'notes']
    success_url = reverse_lazy('appointments:appointment_list')

    def test_func(self):
        appointment = self.get_object()
        return self.request.user == appointment.doctor or self.request.user.is_superuser

class DoctorAvailabilityListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DoctorAvailability
    template_name = 'appointments/availability_list.html'
    context_object_name = 'slots'

    def test_func(self):
        return self.request.user.role == 'doctor' or self.request.user.is_superuser

    def get_queryset(self):
        return DoctorAvailability.objects.filter(doctor=self.request.user)

class DoctorAvailabilityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DoctorAvailability
    template_name = 'appointments/appointment_form.html'
    fields = ['weekday', 'start_time', 'end_time']
    success_url = reverse_lazy('appointments:availability_list')

    def test_func(self):
        return self.request.user.role == 'doctor' or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)
