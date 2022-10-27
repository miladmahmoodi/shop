from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin

from .models import (
    User as UserModel,
    OtpCode as OtpCodeModel,
)
from . import forms
from utils.base_alert import BaseAlert
from utils.sms import send_otp_code

from datetime import (
    datetime,
    timedelta,
)


class UserRegistrationView(View):
    template_name = 'accounts/user_registration.html'
    form_class = forms.UserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:user_login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                'form': self.form_class(),
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # OtpCodeModel.delete_all_codes(data.get('phone_number'))
            OtpCodeModel.send_otp_code(data.get('phone_number'))
            request.session['user_registration_info'] = {
                'email': data.get('email'),
                'phone_number': data.get('phone_number'),
                'full_name': data.get('full_name'),
                'password': data.get('password'),
            }
            messages.success(
                request,
                BaseAlert.success_verify_code,
                'success',
            )
            return redirect('accounts:user_register_verify_code')

        return render(
            request,
            self.template_name,
            {'form': form},
        )


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/user_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                'home:home',
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'form': self.form_class()
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            user = UserModel.objects.filter(
                phone_number=phone_number,
            )
            if not user.exists():
                messages.error(
                    request,
                    BaseAlert.not_register_user,
                    'danger',
                )
                return redirect('accounts:user_login')

            # OtpCodeModel.delete_all_codes(phone_number)
            OtpCodeModel.send_otp_code(phone_number)
            request.session['user_login_info'] = {
                'phone_number': phone_number,
            }
            messages.success(
                request,
                BaseAlert.success_verify_code,
                'success',
            )
            return redirect('accounts:user_login_verify_code')

        return render(
            request,
            self.template_name,
            {
                'form': form,
            },
        )


class UserRegisterVerifyCodeView(View):
    form_class = forms.UserVerifyCodeForm
    template_name = 'accounts/register_verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                'form': self.form_class(),
            }
        )

    def post(self, request):
        user_info = request.session['user_registration_info']
        form = self.form_class(request.POST)
        if form.is_valid():
            user_verify_code = form.cleaned_data['verify_code']
            db_verify_code = OtpCodeModel.objects.filter(
                phone_number=user_info.get('phone_number'),
                code=user_verify_code,
            )
            if not db_verify_code.exists():
                messages.error(
                    request,
                    BaseAlert.wrong_registration_verify_code,
                    'danger',
                )
                return redirect('accounts:user_register_verify_code')

            # expire_verify_code = db_verify_code[0].created_at + timedelta(minutes=1)
            # print('-'*90)
            # print('now:     ', datetime.now().time())
            # print('created: ', db_verify_code[0].created_at.time())
            # print('expire:  ', expire_verify_code.time())
            # print('-'*90)

            if OtpCodeModel.is_expire(user_info.get('phone_number')):
                messages.error(
                    request,
                    BaseAlert.expire_registration_verify_code,
                    'danger',
                )
                db_verify_code.delete()
                return redirect('accounts:user_register')

            UserModel.objects.create_user(
                phone_number=user_info['phone_number'],
                email=user_info['email'],
                full_name=user_info['full_name'],
                password=user_info['password'],
            )
            db_verify_code.delete()
            messages.success(
                request,
                BaseAlert.success_registration,
                'success',
            )
            return redirect('accounts:user_login')
        return render(
            request,
            self.template_name,
            {'form': form},
        )


class UserLoginVerifyCodeView(View):
    form_class = forms.UserVerifyCodeForm
    template_name = 'accounts/register_verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                'form': self.form_class(),
            }
        )

    def post(self, request, *args, **kwargs):
        user_info = request.session['user_login_info']
        form = self.form_class(request.POST)
        if form.is_valid():
            user_verify_code = form.cleaned_data['verify_code']
            db_verify_code = OtpCodeModel.objects.filter(
                phone_number=user_info.get('phone_number'),
                code=user_verify_code,
            )
            if not db_verify_code.exists():
                messages.error(
                    request,
                    BaseAlert.wrong_registration_verify_code,
                    'danger',
                )
                return redirect('accounts:user_login_verify_code')
            db_verify_code.delete()
            user = UserModel.objects.get(
                phone_number=user_info.get('phone_number'),
            )
            login(
                request,
                user,
            )
            messages.success(
                request,
                BaseAlert.success_login,
                'success',
            )
            return redirect('home:home')


class UserLogoutView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        messages.success(
            request,
            BaseAlert.success_logout,
            'success'
        )
        return redirect('home:home')
