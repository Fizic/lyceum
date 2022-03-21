from django.db import models
from django.db.models import Q, CheckConstraint

from Core.models import BaseState, BaseVisibility


class Item(BaseState):
    name = models.CharField(verbose_name='имя товара', max_length=150)
    text = models.TextField(verbose_name="описание", )
    category = models.ForeignKey(to='catalog.Category', verbose_name='категория', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    tags = models.ManyToManyField(to='catalog.Tag', verbose_name="тэги", blank=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(text__icontains=' '), name="min_word_count"),
            CheckConstraint(check=~(Q(text__startswith=' ') | Q(text__endswith=' ')),
                            name='no_spaces_at_the_beginning_and_end'),
            CheckConstraint(check=(Q(text__icontains='превосходно') | Q(text__icontains='роскошно')),
                            name='superb_or_luxurious_in_text')
        ]
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return str(self.name)


class Tag(BaseVisibility):
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return str(self.slug)


class Category(BaseVisibility):
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(weight__lt=32767), name='weight_lt_32767')
        ]
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return str(self.slug)
