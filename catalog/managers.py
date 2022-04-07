from django.db import models
from django.db.models import Prefetch
from catalog import models as catalog_models


class CatalogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch("category_items", queryset=catalog_models.Item.objects.filter(is_published=True))).filter(
            is_published=True).order_by("weight")
