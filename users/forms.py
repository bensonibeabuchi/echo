from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", 'password1', "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class ArticleSearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)
    category = forms.CharField(label='Category', required=False)