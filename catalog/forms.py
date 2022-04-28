from django import forms
from django.db import models


class RatingForm(forms.Form):
    class Feeling(models.IntegerChoices):
        Null = 0, "--------"
        Hatred = 1, 'Ненависть'
        Dislike = 2, 'Неприязнь'
        Neutral = 3, 'Нейтрально'
        Adoration = 4, 'Обожание'
        Love = 5, 'Любовь'

    rating = forms.ChoiceField(choices=Feeling.choices)
