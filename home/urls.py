from django.urls import path, include

from . import views


app_name = 'home'


bucket_url_patterns = [
    path(
        '',
        views.BucketView.as_view(),
        name='bucket',
    ),
    path(
        'bucket/<str:key>/delete/',
        views.BucketDeleteView.as_view(),
        name='bucket_delete',
    ),
    path(
        'bucket/<str:key>/download/',
        views.BucketDownloadView.as_view(),
        name='bucket_download',
    ),
]

urlpatterns = [
    path(
        'bucket/',
        include(bucket_url_patterns),
        # name='bucket',
    ),
    path(
        '',
        views.HomeView.as_view(),
        name='home',
    ),
    path(
        '<slug:category_slug>/',
        views.HomeView.as_view(),
        name='category_filter',
    ),

]