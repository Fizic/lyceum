from django.shortcuts import render

from catalog import models as catalog_models


def home(request):
    template = "homepage/home.html"
    items = catalog_models.Item.objects.order_by("?").all()[:3]
    context = {"items": items}
    return render(request, template, context)
