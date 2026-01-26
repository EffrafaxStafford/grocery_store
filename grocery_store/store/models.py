from django.db import models

from constants import SIZE_CHOICES, MAX_LENGTH_NAME


class SelfNameMixin():
    """Миксин для определения __str__."""

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    

class Category(SelfNameMixin, models.Model):
    """Модель для хранения категории."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=MAX_LENGTH_NAME,
        unique=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True)
    image = models.ImageField(
        upload_to='images/categories/',
        verbose_name='Изображение',
        null=True,
        blank=True,
        default=None)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Subcategory(SelfNameMixin, models.Model):
    """Модель для хранения подкатегории."""

    name = models.CharField(
        verbose_name='Название подкатегории',
        max_length=MAX_LENGTH_NAME,
        unique=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория')
    image = models.ImageField(
        upload_to='images/subcategories/',
        verbose_name='Изображение',
        null=True,
        blank=True,
        default=None)

    class Meta:
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)


class Product(SelfNameMixin, models.Model):
    """Модель для хранения продуктов."""

    name = models.CharField(
        verbose_name='Название продукта',
        max_length=MAX_LENGTH_NAME,
        unique=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True)
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('subcategory', 'name')


class ProductImage(models.Model):
    """Модель для хранения изображении продуктов."""

    image = models.ImageField(
        upload_to='images/products/',
        verbose_name='Изображение',
        null=True,
        blank=True,
        default=None)
    size = models.CharField(
        max_length=MAX_LENGTH_NAME,
        choices=SIZE_CHOICES)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('-size',)
        unique_together = ['product', 'size']
    
    def __str__(self):
        return f'{self.product.slug}_{self.size}_image'
