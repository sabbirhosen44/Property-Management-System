from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Location,
    Property,
    PropertyImage,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage

    extra = 1

    fields = (
        "image",
        "preview",
        "alt_text",
        "is_primary",
        "sort_order",
    )

    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" width="120" />',
                obj.image.url,
            )

        return "No Image"

    preview.short_description = "Preview"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "state",
        "city",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "country",
        "state",
        "city",
    )

    list_filter = (
        "country",
        "state",
        "city",
        "is_active",
    )

    prepopulated_fields = {"slug": ("name",)}

    ordering = (
        "country",
        "city",
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "property_type",
        "status",
        "price",
        "bedrooms",
        "bathrooms",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "address",
    )

    list_filter = (
        "property_type",
        "status",
        "is_featured",
        "is_active",
    )

    prepopulated_fields = {"slug": ("title",)}

    autocomplete_fields = ("location",)

    inlines = [
        PropertyImageInline,
    ]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):

    list_display = (
        "property",
        "thumbnail",
        "is_primary",
        "sort_order",
        "created_at",
    )

    list_filter = ("is_primary",)

    search_fields = (
        "property__title",
        "alt_text",
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.image.url,
            )

        return "No Image"

    thumbnail.short_description = "Thumbnail"
