import random
import string
from django.contrib.auth.models import User
from django.test import Client

from django.test import TestCase

from catalog.models import Item
from users.models import ExtendedUser


class ItemDetailTest(TestCase):
    def setUp(self):
        self.test_item_1 = Item.objects.create(name="test", text="text роскошно")
        self.test_user_1 = ExtendedUser.objects.create_user(email="test@test.com", password="admin")

    def test_item_info(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["item"], self.test_item_1)

    def item_detail_unauthorized_view(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["user"].username, "")

    def item_detail_authorized_view_without_rating(self, email: str, password: str, test_user: User):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(email=email, password=password)
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["user"], test_user)

    def test_item_detail(self):
        for _ in range(10):
            email = ''.join(random.choices(string.ascii_letters, k=10)) + '@test.com'
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            test_user = ExtendedUser.objects.create_user(email=email, password=password)
            self.item_detail_authorized_view_without_rating(email, password, test_user)
            self.item_detail_unauthorized_view()

    def test_item_set_rating(self):
        """
        Если пользователь попытается отправить форму не из графического интерфейса
        """
        client = Client()
        client.login(username="admin", password="admin")
        response = client.post("/catalog/{pk}/".format(pk=self.test_item_1.id), data={"rating": ["6"]})
        self.assertEqual(response.content, b"Rating must be between 0 and 5")
