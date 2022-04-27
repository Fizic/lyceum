from django.db.models import Prefetch
from django.shortcuts import render
from django.views import View

from catalog.models import Item, Tag


class HomeView(View):
    def get(self, request):
        template = "homepage/home.html"

        items = (
            Item.objects.get_all_itmes()
                .prefetch_related(
                Prefetch("tags", queryset=Tag.objects.filter(is_published=True))
            )
                .filter(is_published=True)
                .order_by("?")
                .only("name", "text", "tags__name", "icon_image")[:3]
        )
        is_authenticated = request.user.is_authenticated
        context = {"items": items, "is_authenticated": is_authenticated}
