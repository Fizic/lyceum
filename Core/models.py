from django.db import models


class BaseState(models.Model):
    is_published = models.BooleanField(verbose_name='видимость сущности', default=True)

    class Meta:
        abstract = True
        verbose_name = 'базовое состояние'
        verbose_name_plural = 'базовое состояния'


class BaseVisibility(BaseState):
    slug = models.SlugField(verbose_name='подкаталог сущности', max_length=200)

    class Meta(BaseState.Meta):
        abstract = True
        verbose_name = 'базовая видимость'
        verbose_name_plural = 'базовые видимости'
