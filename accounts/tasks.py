from celery import shared_task
from accounts.models import OtpCode as OtpCodeModel
import pytz
from datetime import datetime, timedelta


@shared_task
def remove_all_expired_otp_code():
    expire_time = datetime.now(
        tz=pytz.timezone('Asia/Tehran'),
    ) - timedelta(minutes=2)

    OtpCodeModel.objects.filter(
        created_at__lt=expire_time,
    ).delete()
