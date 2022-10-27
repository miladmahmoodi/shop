from django.contrib import admin
from .models import (
    Category as CategoryModel,
    Product as ProductModel,
)


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'is_sub',
        'sub_name',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'updated_at',
        'slug',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'image',
        'count',
        'description',
        'price',
        'available',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'name',
        'category',
    )
    list_filter = (
        'updated_at',
        'slug',
        'count',
        'available',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    raw_id_fields = (
        'category',
    )
