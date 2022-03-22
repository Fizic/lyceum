from django.db import models
from django.db.models import Q, CheckConstraint

from core.models import Published, Slug
from . import validators


class Item(Published):
    name = models.CharField('имя товара', max_length=150)
    text = models.TextField(verbose_name="описание", validators=[validators.text_validator])
    category = models.ForeignKey(to='Category', verbose_name='категория', on_delete=models.SET_NULL,
                                 related_name="catalog_items", null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', verbose_name="тэги", related_name="catalog_items", blank=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class Tag(Slug):
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return str(self.slug)


class Category(Slug):
    weight = models.PositiveSmallIntegerField("масса", default=100)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return str(self.slug)
