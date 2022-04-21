from django.contrib.auth.models import User, AbstractUser
from django.db import models


class ExtendedUser(AbstractUser):
    username = models.CharField(unique=False, max_length=256)
    email = models.EmailField(unique=True, max_length=256)
    birthday = models.DateField(verbose_name="День рождения", blank=True, null=True)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = "Расширенный пользователь"
        verbose_name_plural = "Расширенные пользователи"
