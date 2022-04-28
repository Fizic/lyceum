from django.shortcuts import redirect
from django.test import TestCase, Client
from users.models import ExtendedUser


class ItemDetailTest(TestCase):
    def setUp(self) -> None:
        ExtendedUser.objects.create_user(email="test@test.com", password="123")

    def test_login_form(self):
        csrf_client = Client()
        response = csrf_client.post("/auth/login/", data={'email': 'test@test.com', 'password': '123'})
        self.assertRedirects(response, '/auth/profile/')
