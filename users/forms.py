from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import ExtendedUser


class ProfileForm(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    birth_day = forms.DateField(required=False)


class EmailAuthentication(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = ExtendedUser
        fields = ["email"]
