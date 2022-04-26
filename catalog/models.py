import random
from django.db.models import Prefetch
from django.db import models
from PIL import Image
from core.models import Published, Slug
from . import validators
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe


class ItmeManager(models.Manager):
    def get_all_itmes(self):
        return self.get_queryset().prefetch_related("gallery")


class Item(Published):
    name = models.CharField("имя товара", max_length=150)
    text = models.TextField(
        verbose_name="описание",
        validators=[validators.text_validator],
        default=random.choice(["роскошно", "превосходно"]),
    )
    category = models.ForeignKey(
        to="Category",
        verbose_name="категория",
        on_delete=models.SET_NULL,
        related_name="catalog_items",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        to="Tag", verbose_name="тэги", related_name="catalog_items", blank=True
    )
    icon_image = models.ImageField(
        verbose_name="иконка товара", upload_to="uploads/", null=True
    )

    objects = ItmeManager()

    def get_image_100x100(self):
        return get_thumbnail(self.icon_image, "100x100", upscale=False)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class Gallery(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(
        upload_to=f"uploads/", blank=True, verbose_name="Изображения товара"
    )

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "галлерея"

    def get_image(self):
        return get_thumbnail(self.image, "400x400", upscale=False)

    def __str__(self):
        return mark_safe(f"<img src='{self.image.url}' width='200' height='200'>")


class Tag(Slug):
    name = models.CharField("имя тэга", max_length=150)

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"

    def __str__(self):
        return str(self.slug)


class Category(Slug):
    name = models.CharField("название категории", max_length=150)
    weight = models.PositiveSmallIntegerField("масса", default=100)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return str(self.slug)
