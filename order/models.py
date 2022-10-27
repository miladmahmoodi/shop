from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import User as UserModel
from product.models import Product as ProductModel


class Order(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    paid = models.BooleanField(
        default=False,
    )
    discount =  models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.user}'

    def total_price(self):
        total_price = sum(item.cost() for item in self.order_items.all())
        if self.discount:
            discount_price = (total_price / 100) * self.discount
            total_price -= discount_price
        return total_price


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
    )
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(
        default=1
    )

    def __str__(self):
        return f'{self.order}'

    def cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(
        max_length=10,
    )
    discount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code