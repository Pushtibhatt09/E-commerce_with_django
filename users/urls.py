from django.urls import path
from allauth.account.views import LoginView, SignupView

urlpatterns = [
    path("login/", LoginView.as_view(), name="account_login"),
    path("signup/", SignupView.as_view(), name="account_signup"),
]