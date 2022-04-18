from django import forms


class ProfileForm(forms.Form):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    birth_day = forms.DateField(required=False)
