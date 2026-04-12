from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Cart, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:100px;"/>', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Preview'


# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)