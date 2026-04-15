from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('add/<int:appointment_id>/', views.MedicalRecordCreateView.as_view(), name='add_record'),
    path('<int:pk>/', views.MedicalRecordDetailView.as_view(), name='record_detail'),
    path('<int:record_id>/request-access/', views.request_medical_record_access, name='request_access'),
    path('approve-request/<int:request_id>/', views.approve_medical_record_access, name='approve_access'),
]
