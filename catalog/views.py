from django.shortcuts import render, redirect
from django.views import View

from catalog.models import Category, Item
from rating.models import Rating
from catalog.forms import RatingForm
from catalog.services import get_item_information


class ItemListView(View):
    def get(self, request):
        template = "catalog/item_list.html"
        categories = Category.objects.categories_and_items()
        context = {
            'categories': categories,
            'user': request.user
        }
        return render(request, template, context)


class ItemDetailView(View):
    def get(self, request, pk: int):
        template = "catalog/item_detail.html"
        context = get_item_information(request, pk)
        return render(request, template, context)

    def post(self, request, pk: int):
        form = RatingForm(request.POST)

        if form.is_valid():
            item = Item.objects.get(pk=pk)
            user_star, _ = Rating.objects.get_or_create(user=request.user, item=item, defaults={'star': 0})
            user_star.star = form.cleaned_data['stars']
            user_star.save()
            return redirect('item_detail', pk)
