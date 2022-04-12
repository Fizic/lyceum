from django.db.models import Prefetch, Avg
from django.shortcuts import get_object_or_404

from catalog.forms import RatingForm
from catalog.models import Item, Tag
from rating.models import Rating


def get_item_information(request, item_id: int) -> dict:
    """
    Получения данных о товаре, в зависимости от статуса пользователя.

    :param request: запрос
    :param item_id: id товара
    :return: context for html template
    """
    item = get_object_or_404(
        Item.objects.prefetch_related(
            Prefetch("tags", queryset=Tag.objects.filter(is_published=True))
        ).select_related(
            "category"
        ).only("name", "text", "category__name", "tags__name"), id=item_id
    )

    all_rating_for_item = Rating.objects.filter(item_id=item_id)
    average_rating = all_rating_for_item.aggregate(Avg('star'))["star__avg"]
    rating_count = all_rating_for_item.count()

    context = {
        "item": item,
        "average_rating": average_rating,
        "rating_count": rating_count
    }

    if request.user.is_authenticated:
        context["user"] = request.user
        context["rating"] = get_object_or_404(Rating.objects, user=request.user, item_id=item_id)
        context["form"] = RatingForm()

    return context
