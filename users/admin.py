from django.contrib import admin
from .forms import CustomUserCreationForm
from users.models import ExtendedUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(ExtendedUser)
class ExtendedUserAdmin(BaseUserAdmin):
    model = ExtendedUser
    list_display = ("email", "username", "is_staff")
    list_filter = ("is_staff",)
    add_form = CustomUserCreationForm
    ordering = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
