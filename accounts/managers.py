from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

from utils.base_alert import BaseAlert


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValidationError(BaseAlert.must_have_phone_number)
        if not email:
            raise ValidationError(BaseAlert.must_have_email)
        if not full_name:
            raise ValidationError(BaseAlert.must_have_full_name)

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(
            phone_number,
            email,
            full_name,
            password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
