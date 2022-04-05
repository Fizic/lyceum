from django.http import Http404
from django.shortcuts import render
from . import models as catalog_models
from django.core.exceptions import ObjectDoesNotExist


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog_models.Item.objects.order_by("?").filter(is_published=True)
    context = {"items": items}
    return render(request, template, context)


def item_detail(request, pk: int):
    template = "catalog/item_detail.html"
    try:
        item = catalog_models.Item.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404
    context = {"item": item}
    return render(request, template, context)
