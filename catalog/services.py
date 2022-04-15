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
    rating_count = all_rating_for_item.count()

    if rating_count:
        average_rating = all_rating_for_item.aggregate(Avg('star'))["star__avg"]
    else:
        average_rating = 0

    context = {
        "item": item,
        "average_rating": average_rating,
        "rating_count": rating_count
    }

    if not request.user.is_authenticated:
        return context

    context["form"] = RatingForm()
    context["user"] = request.user
    if all_rating_for_item.filter(user=request.user).count():
        context["rating"] = Rating.objects.get(user=request.user, item_id=item_id)
    else:
        context["rating"] = {"star": 0}

    return context
