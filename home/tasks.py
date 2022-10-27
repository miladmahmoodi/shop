from bucket import bucket
from celery import shared_task

# TODO:
def get_all_objects_task():
    buckets = bucket.get_objects()
    return buckets


@shared_task
def delete_object_task(key):
    bucket.delete_object(key)


@shared_task
def download_object_task(key):
    bucket.download_object(key)
