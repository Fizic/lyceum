from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from catalog import models
from django.core.exceptions import ObjectDoesNotExist


def item_list(request):
    template = "catalog/item_list.html"
    items = models.Item.objects.prefetch_related(
        Prefetch("tags", queryset=models.Tag.objects.filter(is_published=True))).order_by("?").filter(is_published=True)
    context = {"items": items}

    return render(request, template, context)


def item_detail(request, pk: int):
    template = "catalog/item_detail.html"
    item = get_object_or_404(
        models.Item.objects.prefetch_related(Prefetch("tags", queryset=models.Tag.objects.filter(is_published=True))),
        id=pk)
    context = {"item": item}

    return render(request, template, context)
