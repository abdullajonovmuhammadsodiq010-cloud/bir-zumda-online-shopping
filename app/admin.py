from django.contrib import admin

from app.models import ProductModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'discount', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category', 'description')
    list_per_page = 25
    ordering = ('-created_at',)
