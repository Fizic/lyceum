from django.contrib import admin
from django.contrib.auth.models import User

from users.models import UserWithBirthday


class UserWithBirthdayInline(admin.StackedInline):
    model = UserWithBirthday


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserWithBirthdayInline
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
