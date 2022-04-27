from django.contrib import admin
from users.forms import CustomUserCreationForm
from users.models import ExtendedUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _



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
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "birthday")}),
    )
