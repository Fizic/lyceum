from django import forms

from rating.models import Rating


class RatingForm(forms.Form):
    stars = forms.ChoiceField(choices=Rating.Feeling.choices, label='Выберите свое отношение', widget=forms.RadioSelect)
