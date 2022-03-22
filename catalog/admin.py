from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_display_links = ('name',)
    list_editable = ('is_published',)
    filter_horizontal = ('tags',)


admin.site.register(models.Item, ItemAdmin)


class TagAdmin(admin.ModelAdmin):
    fields = ('is_published', 'slug')


admin.site.register(models.Tag, TagAdmin)


class CategoryAdmin(admin.ModelAdmin):
    fields = ('is_published', 'slug', 'weight')


admin.site.register(models.Category, CategoryAdmin)
