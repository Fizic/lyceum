import random
from django.db.models import Prefetch
from django.db import models
from django.db.models import Prefetch

from PIL import Image
from core.models import Published, Slug
from . import validators
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe


class ItemManager(models.Manager):
    def get_all_items(self):
        return self.get_queryset().prefetch_related("gallery")

    def published_tags(self):
        return self.get_queryset().filter(is_published=True).only('name', 'text').prefetch_related(
            Prefetch('tags', queryset=Tag.objects.filter(is_published=True).only('name')))


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

    objects = ItemManager()

    def get_image_100x100(self):
        return get_thumbnail(self.icon_image, "100x100", upscale=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.icon_image:
            image = Image.open(self.icon_image.path)
            if image.height > 100 or image.width > 100:
                image.thumbnail((100, 100), Image.ANTIALIAS)
                image.save(self.icon_image.path)

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.height > 400 or image.width > 400:
                image.thumbnail((400, 400), Image.ANTIALIAS)
                image.save(self.image.path)


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
