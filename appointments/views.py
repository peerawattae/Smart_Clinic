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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_appointments = self.get_queryset()
        context['active_appointments'] = all_appointments.filter(
            status__in=['pending', 'confirmed']
        )
        context['history_appointments'] = all_appointments.filter(
            status__in=['completed', 'cancelled', 'no_show']
        )
        return context


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

from .forms import AppointmentForm

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:appointment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        if user.role == 'doctor':
            form.instance.doctor = user
        elif user.role == 'patient':
            form.instance.patient = user
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
