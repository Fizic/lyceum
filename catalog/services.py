from django.db.models import Prefetch, Avg, Count
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

    stars = Rating.objects.filter(item=item, star__in=list(
        filter(lambda x: x != 0, map(lambda y: y[0], Rating.Feeling.choices)))).aggregate(Avg('star'), Count('star'))

    context = {
        "item": item,
        'stars': stars,
        'user': request.user
    }

    if not request.user.is_authenticated:
        return context

    context["form"] = RatingForm()
    context["user_star"] = Rating.objects.filter(user=request.user, item=item).first()

    return context
