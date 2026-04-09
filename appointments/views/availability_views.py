from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..models import DoctorAvailability

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
