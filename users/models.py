from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Почта должна быть указана в обязательном порядке.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Админимтраторы должны быть определенны с is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class ExtendedUser(AbstractUser):
    username = models.CharField(unique=False, max_length=256, blank=True)
    email = models.EmailField(unique=True, max_length=256)
    birthday = models.DateField(verbose_name="День рождения", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_birthday(self):
        return self.birthday.strftime("%m-%d")

    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ["email"]
        verbose_name = "Расширенный пользователь"
        swappable = "AUTH_USER_MODEL"
        verbose_name_plural = "Расширенные пользователи"
