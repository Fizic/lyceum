from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


def get_birthday_people(request):
    cur_date = date.today()
    birth_today = User.objects.filter(birthday=cur_date).values("email")
    return {"birth_today": birth_today}
