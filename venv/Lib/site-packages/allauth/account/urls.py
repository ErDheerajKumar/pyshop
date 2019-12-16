from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r"^signup/$", views.signup, name="account_signup"),
    re_path(r"^login/$", views.login, name="account_login"),
    re_path(r"^logout/$", views.logout, name="account_logout"),

    re_path(r"^password/change/$", views.password_change,
        name="account_change_password"),
    re_path(r"^password/set/$", views.password_set, name="account_set_password"),

    re_path(r"^inactive/$", views.account_inactive, name="account_inactive"),

    # E-mail
    re_path(r"^email/$", views.email, name="account_email"),
    re_path(r"^confirm-email/$", views.email_verification_sent,
        name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
        name="account_confirm_email"),

    # password reset
    re_path(r"^password/reset/$", views.password_reset,
        name="account_reset_password"),
    re_path(r"^password/reset/done/$", views.password_reset_done,
        name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key"),
    re_path(r"^password/reset/key/done/$", views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"),
]
