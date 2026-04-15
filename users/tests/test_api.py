from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Notification

User = get_user_model()

class UserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.notif = Notification.objects.create(user=self.user, title="Test", message="Msg")

    def test_delete_notification_api(self):
        url = reverse('delete_notification', kwargs={'pk': self.notif.pk})
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertFalse(Notification.objects.filter(pk=self.notif.pk).exists())

    def test_clear_all_notifications_api(self):
        url = reverse('clear_all_notifications')
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(self.user.notifications.count(), 0)
