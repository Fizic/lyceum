from django.contrib.auth.models import User
from django.test import Client

from django.test import TestCase

from catalog.models import Item


class ItemDetailTest(TestCase):
    def setUp(self):
        self.test_item_1 = Item.objects.create(name="test", text="text роскошно")
        User.objects.create_user(username="admin", password="admin")

    def test_item_info(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["item"].name, "test")
        self.assertEqual(response.context["item"].text, "text роскошно")

    def test_item_detail_unauthorized_view(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["user"].username, "")

    def test_item_detail_authorized_view_without_rating(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username="admin", password="admin")
        response = csrf_client.get("/catalog/{pk}/".format(pk=self.test_item_1.id))
        self.assertEqual(response.context["user"].username, "admin")

    def test_item_set_rating(self):
        """
        Если пользователь попытается отправить форму не из графического интерфейса
        """
        client = Client()
        client.login(username="admin", password="admin")
        response = client.post("/catalog/{pk}/".format(pk=self.test_item_1.id), data={"rating": ["6"]})
        self.assertEqual(response.content, b"Rating must be between 0 and 5")
