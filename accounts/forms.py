from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import get_object_or_404

from .models import (
    User as UserModel,
    OtpCode as OtpCodemodel,
)
from utils.base_alert import BaseAlert


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Password...'
            }
        ),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password...'
            }
        ),
    )

    class Meta:
        model = UserModel
        fields = (
            'full_name',
            'email',
            'phone_number',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Full Name...',
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Email...',
                },
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Phone Number...',
                },
            ),
        }

    def clean_email(self):
        register_email = self.cleaned_data['email']
        user = UserModel.objects.filter(
            email=register_email,
        )
        if user.exists():
            raise ValidationError(BaseAlert.register_email_exist)
        return register_email

    def clean_phone_number(self):
        register_phone_number = self.cleaned_data['phone_number']
        user = UserModel.objects.filter(
            phone_number=register_phone_number,
        )
        if user.exists():
            raise ValidationError(BaseAlert.register_phone_number_exist)
        OtpCodemodel.delete_all_codes(register_phone_number)
        return register_phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError(BaseAlert.confirm_password)
        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data['password']
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=BaseAlert.change_password_help_text,
    )

    class Meta:
        model = UserModel
        fields = '__all__'


class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name...'
            }
        ),
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Email...'
            }
        ),
    )
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number...'
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Password...'
            }
        ),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password...'
            }
        ),
    )

    # class Meta:
    #     model = UserModel
    #     fields = (
    #         'full_name',
    #         'email',
    #         'phone_number',
    #     )
    #     widgets = {
    #         'full_name': forms.TextInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'placeholder': 'Your Full Name...',
    #             },
    #         ),
    #         'email': forms.EmailInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'placeholder': 'Your Email...',
    #             },
    #         ),
    #         'phone_number': forms.TextInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'placeholder': 'Your Phone Number...',
    #             },
    #         ),
    #     }

    def clean_email(self):
        register_email = self.cleaned_data['email']
        user = UserModel.objects.filter(
            email=register_email,
        )
        if user.exists():
            raise ValidationError(BaseAlert.register_email_exist)
        return register_email

    def clean_phone_number(self):
        register_phone_number = self.cleaned_data['phone_number']
        user = UserModel.objects.filter(
            phone_number=register_phone_number,
        )
        if user.exists():
            raise ValidationError(BaseAlert.register_phone_number_exist)
        return register_phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError(BaseAlert.confirm_password)
        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data['password']
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserVerifyCodeForm(forms.Form):
    verify_code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Verify Code...',
            }
        ),
    )


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Phone Number...',
            },
        ),
    )

    def clean_phone_number(self):
        login_phone_number = self.cleaned_data['phone_number']
        user = UserModel.objects.filter(
            phone_number=login_phone_number,
        )
        if not user.exists():
            raise ValidationError(BaseAlert.not_register_user)

        OtpCodemodel.delete_all_codes(login_phone_number)
        return login_phone_number

