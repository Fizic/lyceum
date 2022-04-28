from django.db.models import Prefetch
from django.shortcuts import render

from catalog.models import Item, Category, Tag


def home(request):
    template = "homepage/home.html"
    items = Item.objects.prefetch_related(Prefetch("tags", queryset=Tag.objects.filter(is_published=True))).filter(
        is_published=True).order_by("?").only("name", "text", "tags__name")[:3]
    is_authenticated = request.user.is_authenticated
    context = {"items": items, "is_authenticated": is_authenticated}

    return render(request, template, context)
