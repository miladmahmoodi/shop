from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path(
        'register/',
        views.UserRegistrationView.as_view(),
        name='user_register',
    ),
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='user_login',
    ),
    path(
        'logout/',
        views.UserLogoutView.as_view(),
        name='user_logout',
    ),
    path(
        'register/verify/code/',
        views.UserRegisterVerifyCodeView.as_view(),
        name='user_register_verify_code',
    ),
    path(
        'login/verify/code/',
        views.UserLoginVerifyCodeView.as_view(),
        name='user_login_verify_code',
    ),
]
