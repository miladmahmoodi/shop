from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path(
        'cart/',
        views.CartView.as_view(),
        name='cart',
    ),
    path(
        'add/<int:product_id>/',
        views.CartAddView.as_view(),
        name='cart_add',
    ),
    path(
        'remove/<int:product_pk>/',
        views.CartRemoveView.as_view(),
        name='cart_remove',
    ),
    path(
        'checkout/',
        views.OrderCheckoutView.as_view(),
        name='checkout',
    ),
    path(
        'checkout/detail/<int:order_pk>/',
        views.OrderCheckoutDetailView.as_view(),
        name='checkout_detail',
    ),
    path(
        'checkout/coupon/<int:order_id>/',
        views.CheckoutCouponView.as_view(),
        name='checkout_coupon',
    ),

]
