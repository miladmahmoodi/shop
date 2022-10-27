from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import (
    Product as ProductModel,
)
from order.forms import CartAddForm


class ProductDetailView(View):
    template_name = 'product/detail.html'
    form_class = CartAddForm

    def get(self, request, slug):
        product = get_object_or_404(
            ProductModel,
            slug=slug,
        )
        return render(
            request,
            self.template_name,
            {
                'product': product,
                'form': self.form_class()
            }
        )