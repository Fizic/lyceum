from django.db import models


class Published(models.Model):
    is_published = models.BooleanField(verbose_name='опубликовано', default=True)

    class Meta:
        abstract = True
        verbose_name = 'состояние'
        verbose_name_plural = 'состояния'


class Slug(Published):
    slug = models.SlugField(verbose_name='слэг', max_length=200)

    class Meta(Published.Meta):
        abstract = True
        verbose_name = 'подкаталог'
        verbose_name_plural = 'подкаталоги'
