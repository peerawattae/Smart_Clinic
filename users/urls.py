from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('all-patients/', views.all_patients, name='all_patients'),
    path('approve-doctor/<int:user_id>/', views.approve_doctor, name='approve_doctor'),
    path('toggle-staff/<int:user_id>/', views.toggle_staff_status, name='toggle_staff_status'),
    path('edit-staff/<int:user_id>/', views.edit_staff, name='edit_staff'),
    path('profile/', views.profile_view, name='profile'),
]


