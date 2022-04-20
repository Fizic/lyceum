from django import forms


class ProfileForm(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    birth_day = forms.DateField(required=False)


class EmailAuthentication(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
