from django.urls import path
from .views import AppointmentListView, AppointmentDetailView, AppointmentCreateView

app_name = 'appointments'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('new/', AppointmentCreateView.as_view(), name='appointment_create'),
]
