from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from product.models import (
    Product as ProductModel,
    Category as CategoryModel,
)
from . import tasks
from utils.base_alert import BaseAlert
from utils.mixins import IsAdminUserMixin


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request, category_slug=None):
        categories = CategoryModel.objects.filter(
            is_sub=False,
        )
        products = ProductModel.objects.filter(
            available=True,
        )

        if category_slug:
            category = CategoryModel.objects.get(
                slug=category_slug,
            )
            products = category.products.all()

        return render(
            request,
            self.template_name,
            {
                'products': products,
                'categories': categories,
            }
        )


class BucketView(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        buckets = tasks.get_all_objects_task()
        return render(
            request,
            self.template_name,
            {
                'buckets': buckets,
            }
        )


class BucketDeleteView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(
            request,
            BaseAlert.success_delete_bucket,
            'success',
        )
        return redirect('home:bucket')


class BucketDownloadView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(
            request,
            BaseAlert.success_download_bucket,
            'success',
        )
        return redirect('home:bucket')