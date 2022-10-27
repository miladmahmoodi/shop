from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(
        max_length=125,
        unique=True,
    )
    slug = models.SlugField(
        max_length=125,
        unique=True,
    )
    is_sub = models.BooleanField(
        default=False,
    )
    sub_name = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            'name',
        )
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'home:category_filter',
            args=[
                self.slug,
            ]
        )


class Product(models.Model):
    category = models.ManyToManyField(
        Category,
        default=None,
        related_name='products',
    )
    name = models.CharField(
        max_length=125,
        unique=True,
    )
    slug = models.SlugField(
        max_length=125,
        unique=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )
    count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    description = RichTextField(
        config_name='default'
    )
    price = models.IntegerField(
        null=True,
        blank=True,
    )
    available = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'product:product_detail',
            args=[
                self.slug,
            ]
        )
