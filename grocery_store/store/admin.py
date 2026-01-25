from django.contrib import admin

from .models import Category, Subcategory, Product, ProductImage
from constants import SIZE_CHOICES


class SlugAutoFillMixin():
    """Миксин для автозаполнения поля slug."""

    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        abstract = True

class SearchFieldNameMixin():
    """Миксин для поиска по name."""

    search_fields = ('name',)

    class Meta:
        abstract = True


@admin.register(Category)
class CategoryAdmin(SlugAutoFillMixin, SearchFieldNameMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image')


@admin.register(Subcategory)
class SubcategoryAdmin(SlugAutoFillMixin, SearchFieldNameMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image', 'category')


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = len(SIZE_CHOICES)


@admin.register(Product)
class ProductAdmin(SlugAutoFillMixin, SearchFieldNameMixin, admin.ModelAdmin):
    inlines = (ProductImageInline,)
    list_display = ('id', 'name', 'slug', 'price', 'subcategory')
    
