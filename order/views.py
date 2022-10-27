from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from product.models import Product as ProductModel
from .forms import CartAddForm, CouponForm
from .cart import Cart
from utils.base_alert import BaseAlert
from .models import (
    Order as OrderModel,
    OrderItem as OrderItemModel,
    Coupon as CouponModel,
)

from datetime import datetime
import pytz


class CartView(View):
    template = 'order/cart.html'
    form_class = CouponForm

    def get(self, request):
        cart = Cart(request)

        return render(
            request,
            self.template,
            {
                'cart': cart,
                'form': self.form_class()
            }
        )


class CartAddView(View):
    form_class = CartAddForm

    def post(self, request, product_id):
        form = self.form_class(request.POST)
        cart = Cart(request)
        product = get_object_or_404(
            ProductModel,
            pk=product_id,
        )

        if form.is_valid():
            cart.add(
                product,
                form.cleaned_data.get('quantity'),
            )
        messages.success(
            request,
            BaseAlert.success_add_to_cart,
            'success',
        )
        return redirect('order:cart')


class CartRemoveView(View):
    def get(self, request, product_pk):
        cart = Cart(request)
        product = get_object_or_404(
            ProductModel,
            pk=product_pk,
        )
        cart.remove(product)
        messages.success(
            request,
            BaseAlert.success_remove_product,
            'success',
        )
        return redirect('order:cart')


class OrderCheckoutView(LoginRequiredMixin, View):
    permission_required = ()

    def get(self, request):
        cart = Cart(request)
        if cart:
            order = OrderModel.objects.create(
                user=request.user,
            )
            for item in cart:
                OrderItemModel.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            messages.success(
                request,
                BaseAlert.success_checkout,
                'success',
            )
            cart.clear()
            return redirect('order:checkout_detail', order.pk)
        return redirect('home:home')


class OrderCheckoutDetailView(LoginRequiredMixin, View):
    template_name = 'order/checkout_detail.html'
    form_class = CouponForm

    def get(self, request, order_pk):
        order = get_object_or_404(
            OrderModel,
            pk=order_pk,
        )
        return render(
            request,
            self.template_name,
            {
                'order': order,
                'form': self.form_class(),
            }
        )


class CheckoutCouponView(LoginRequiredMixin, View):
    form_class = CouponForm
    template_name = 'order/checkout_detail.html'

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        datetime_now = datetime.now(
            tz=pytz.timezone('Asia/Tehran'),
        )
        order = get_object_or_404(
            OrderModel,
            pk=order_id,
        )
        if form.is_valid():
            try:
                coupon = CouponModel.objects.get(
                    code__exact=form.cleaned_data.get('code'),
                    valid_from__lte=datetime_now,
                    valid_to__gte=datetime_now,
                    active=True,
                )
            except CouponModel.DoesNotExist:
                messages.error(
                    request,
                    BaseAlert.wrong_coupon,
                    'danger',
                )
                return redirect(
                    'order:checkout_detail',
                    order_id,
                )
            order.discount = coupon.discount
            order.save()
            messages.success(
                request,
                BaseAlert.success_coupon,
                'success',
            )
            return redirect(
                'order:checkout_detail',
                order_id,
            )

        return render(
            request,
            self.template_name,
            {
                'order': order,
                'form': self.form_class(),
            }
        )
