"""Circles URLs."""

# Django
from django.urls import path

# Views
from .views.users import LoginView,LogoutView,IndexView,SignUpView,ActivateAccount,EmailConfirmView

urlpatterns = [
    path('',LoginView.as_view(),name="login"),
    path('users/logout',LogoutView.as_view(),name="logout"),
    path('users/index',IndexView.as_view(),name="index"),
    path('users/signup',SignUpView.as_view(),name="signup"),
    path('users/email_confirm',EmailConfirmView.as_view(),name="email_confirm"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]