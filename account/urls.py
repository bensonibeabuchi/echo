from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [

       path('login/', login_page, name='login'),  # noqa
       path('logout/', logout_user, name='logout'),  # noqa
       path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),  # noqa
       path('account_invalid_link/', account_invalid_link, name='account_invalid_link'),  # noqa
       path('register/', register_page, name='register'),  # noqa 
       path('account_activation_complete/', account_activation_complete, name='account_activation_complete'),  # noqa
       path('activate/<uidb64>/<token>/', activate, name='activate'),  # noqa

       path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password-reset'),  # noqa
       path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),  # noqa
       path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),  # noqa
       path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),  # noqa

]
