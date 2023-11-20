from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("acccounts/change-password/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="change_password"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("profile/", views.profile, name="profile"),
]