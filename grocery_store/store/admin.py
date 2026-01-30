from django.contrib import admin

from .models import Category, Subcategory, Product, ProductImage
from constants import SIZE_CHOICES


class SlugAutoFillSearchDisplayMixin():
    """
    Миксин для автозаполнения поля slug,
    поиска по name и кликабельных полей.
    """

    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_display_links = ['id', 'name', 'slug']

    class Meta:
        abstract = True


@admin.register(Category)
class CategoryAdmin(SlugAutoFillSearchDisplayMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Subcategory)
class SubcategoryAdmin(SlugAutoFillSearchDisplayMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category')


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = len(SIZE_CHOICES)


@admin.register(Product)
class ProductAdmin(SlugAutoFillSearchDisplayMixin, admin.ModelAdmin):
    inlines = (ProductImageInline,)
    list_display = ('id', 'name', 'slug', 'price', 'subcategory')
