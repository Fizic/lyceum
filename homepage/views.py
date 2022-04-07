from django.db.models import Prefetch
from django.shortcuts import render

from catalog import models


def home(request):
    template = "homepage/home.html"
    items = models.Item.objects.prefetch_related(Prefetch("tags", queryset=models.Tag.objects.filter(is_published=True))).filter(is_published=True).order_by("?")[:3]
    context = {"items": items}

    return render(request, template, context)
