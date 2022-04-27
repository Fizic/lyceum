from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import ExtendedUser


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты', max_length=254, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ExtendedUser
        fields = ['email', 'username', 'birthday']


class BeautifulPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class BeautifulAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )


class BeautifulSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class BeautifulPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )


class BeautifulUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BeautifulUserCreationForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = ExtendedUser
        fields = ('email', 'password1', 'password2')
