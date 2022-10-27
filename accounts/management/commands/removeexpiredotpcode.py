from django.core.management.base import BaseCommand
from accounts.models import OtpCode as OtpCodeModel

from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'remove all expired otp code.'

    def handle(self, *args, **options):
        expired_time = datetime.now(
            tz=pytz.timezone('Asia/Tehran'),
        ) - timedelta(minutes=2)
        OtpCodeModel.objects.filter(
            created_at__lt=expired_time,
        ).delete()
        self.stdout.write(
            self.style.SUCCESS('Successfully delete expired otp code.')
        )
