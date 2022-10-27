from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . import managers
from utils.sms import send_otp_code

from random import randint
from datetime import datetime, timedelta

import pytz


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=250,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
    )
    full_name = models.CharField(
        max_length=128,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )

    objects = managers.UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [
        'email',
        'full_name',
    ]

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(
        max_length=11,
    )
    code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.phone_number}'

    @classmethod
    def send_otp_code(cls, phone_number):
        otp_code = randint(1000, 9999)
        send_otp_code(
            phone_number,
            otp_code,
        )
        cls.objects.create(
            phone_number=phone_number,
            code=otp_code,
        )

    @classmethod
    def is_expire(cls, phone_number):
        db_verify_code = cls.objects.filter(
            phone_number=phone_number,
        ).last()
        expire_verify_code = datetime.now(
            tz=pytz.timezone('Asia/Tehran'),
        ) - timedelta(minutes=2)

        if db_verify_code.created_at < expire_verify_code:
            return True
        return False

    @classmethod
    def delete_all_codes(cls, phone_number):
        OtpCode.objects.filter(
            phone_number=phone_number,
        ).delete()
