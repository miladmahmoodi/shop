from django.contrib import admin

from order.models import (
    Order as OrderModel,
    OrderItem as OrderItemModel,
    Coupon as CouponModel,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    # can_delete = False
    raw_id_fields = (
        'product',
    )


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'user',
    )
    inlines = (
        OrderItemInline,
    )
    list_display = (
        'user',
        'paid',
        'created_at',
        'updated_at',
    )


@admin.register(CouponModel)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount',
        'active',
        'created_at',
        'updated_at',
        'valid_from',
        'valid_to',
    )
