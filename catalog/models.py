import random

from django.db import models
from django.db.models import Prefetch

from core.models import Published, Slug
from . import validators


class ItemManager(models.Manager):
    def published_tags(self):
        return self.get_queryset().filter(is_published=True).only('name', 'text').prefetch_related(
            Prefetch('tags', queryset=Tag.objects.filter(is_published=True).only('name')))


class Item(Published):
    name = models.CharField("имя товара", max_length=150)
    text = models.TextField(verbose_name="описание", validators=[validators.text_validator],
                            default=random.choice(["роскошно", "превосходно"]))
    category = models.ForeignKey(to="Category", verbose_name="категория", on_delete=models.SET_NULL,
                                 related_name="items", null=True, blank=True)
    tags = models.ManyToManyField(to="Tag", verbose_name="тэги", related_name="catalog_items", blank=True)
    objects = ItemManager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class Tag(Slug):
    name = models.CharField("имя тэга", max_length=150)

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return str(self.slug)


class CategoryManager(models.Manager):
    def categories_and_items(self):
        return self.get_queryset().filter(is_published=True).only('name').prefetch_related(
            Prefetch('items', queryset=Item.objects.filter(is_published=True))).prefetch_related(
            Prefetch('items__tags', queryset=Tag.objects.filter(is_published=True).only('name')))


class Category(Slug):
    name = models.CharField("название категории", max_length=150)
    weight = models.PositiveSmallIntegerField("масса", default=100)
    objects = CategoryManager()

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return str(self.slug)
