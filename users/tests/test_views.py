from django.test import TestCase
from django.urls import reverse

class UserViewTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
