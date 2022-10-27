import boto3
import logging
from botocore.exceptions import ClientError

from django.conf import settings


class Bucket:
    """CDN Bucket manager
    init method creates connection.
    NOTE:
    none of these methods are async. use public interface in tasks.py modules instead.
    """

    def __init__(self):
        self.resource = boto3.resource(
            settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def get_objects(self):
        # result = self.conn.list_objects_v2(
        #     Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        # )
        # if result['KeyCount']:
        #     return result['Contents']
        # else:
        #     return None

        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            bucket = self.resource.Bucket(bucket_name)
            return bucket.objects.all()

        except ClientError as e:
            logging.error(e)

    def delete_object(self, key):
        # self.conn.delete_object(
        #     Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        #     Key=key,
        # )
        # return True
        try:
            # bucket
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            bucket = self.resource.Bucket(bucket_name)
            object = bucket.Object(key)

            response = object.delete(
                VersionId='string',
            )
            return True
        except Exception:
            print('has exception')

    def download_object(self, key):
        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            bucket = self.resource.Bucket(bucket_name)

            bucket.download_file(
                key,
                settings.AWS_LOCAL_STORAGE,
            )
        except Exception:
            print('has exception')


bucket = Bucket()
