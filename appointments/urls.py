from django.urls import path
from .views import (
    AppointmentListView, 
    AppointmentDetailView, 
    AppointmentCreateView,
    AppointmentUpdateView,
    DoctorAvailabilityListView,
    DoctorAvailabilityCreateView,
    get_taken_slots
)

app_name = 'appointments'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('get-taken-slots/', get_taken_slots, name='get_taken_slots'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('new/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('availability/', DoctorAvailabilityListView.as_view(), name='availability_list'),
    path('availability/new/', DoctorAvailabilityCreateView.as_view(), name='availability_create'),
]
