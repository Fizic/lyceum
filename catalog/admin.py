from django.contrib import admin

from . import models


class GalleryAdmin(admin.TabularInline):
    model = models.Gallery
    can_delete = False
    extra = 1
    max_num = 100


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = (GalleryAdmin,)
    list_display = ("name", "is_published")
    list_display_links = ("name",)
    list_editable = ("is_published",)
    filter_horizontal = ("tags",)
    save_on_top = True

    class Meta:
        model = models.Item


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ("is_published", "slug", "name")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("is_published", "slug", "name", "weight")
