from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from ..models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'users/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.user.notifications.filter(is_read=False).update(is_read=True)
        return context

@login_required
def delete_notification(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        request.user.notifications.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
