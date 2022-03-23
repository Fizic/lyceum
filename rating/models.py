from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class Rating(models.Model):
    user = models.ForeignKey(User, verbose_name="пользователь", on_delete=models.CASCADE)
    item = models.ForeignKey(to='catalog.Item', verbose_name="товар", on_delete=models.CASCADE)

    class Feeling(models.IntegerChoices):
        Hatred = 1, 'Ненависть'
        Dislike = 2, 'Неприязнь'
        Neutral = 3, 'Нейтрально'
        Adoration = 4, 'Обожание'
        Love = 5, 'Любовь'

    star = models.PositiveSmallIntegerField(verbose_name='кол-во звезд', choices=Feeling.choices, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'item'], name='item_rating_unique')
        ]
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'

    def __str__(self):
        return str(self.user) + ' ' + str(self.item) + ' ' + str(self.star)