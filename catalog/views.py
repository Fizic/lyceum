from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from catalog.models import Tag, Item
from rating.models import Rating
from catalog.forms import RatingForm
from catalog.services import get_item_information


def item_list(request):
    template = "catalog/item_list.html"
    items = Item.objects.prefetch_related(
        Prefetch("tags", queryset=Tag.objects.filter(is_published=True))).order_by("?").filter(is_published=True).only(
        "name", "text", "tags__name"
    )
    context = {"items": items}

    return render(request, template, context)


class ItemDetailView(View):
    def get(self, request, pk: int):
        template = "catalog/item_detail.html"
        context = get_item_information(request, pk)
        return render(request, template, context)

    def post(self, request, pk: int):
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = get_object_or_404(Rating.objects, user=request.user, item_id=pk)
            rating.star = int(form.cleaned_data["rating"][0])
            rating.save()

            return HttpResponseRedirect("/auth/users/{user_id}/".format(user_id=request.user.id))
        else:
            return HttpResponse("Sorry we can't process your request.")