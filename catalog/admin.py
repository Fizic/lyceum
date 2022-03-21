from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_display_links = ('name',)
    list_editable = ('is_published',)
    filter_horizontal = ('tags', )


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Category)
