from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from catalog.models import Tag, Item


def item_list(request):
    template = "catalog/item_list.html"
    items = Item.objects.prefetch_related(
        Prefetch("tags", queryset=Tag.objects.filter(is_published=True))).order_by("?").filter(is_published=True).only("tags")
    context = {"items": items}

    return render(request, template, context)


def item_detail(request, pk: int):
    template = "catalog/item_detail.html"
    item = get_object_or_404(
        Item.objects.prefetch_related(Prefetch("tags", queryset=Tag.objects.filter(is_published=True))).only("tags"),
        id=pk)
    context = {"item": item}

    return render(request, template, context)
