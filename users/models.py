from django.contrib.auth.models import User
from django.db import models


class UserWithBirthday(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name="День рождения", blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Расширенный пользователь"
        verbose_name_plural = "Расширенные пользователи"
