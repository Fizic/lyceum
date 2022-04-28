from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


def get_birthday_people(request):
    cur_date_month, cur_date_day = date.today().strftime("%m"), date.today().strftime(
        "%d"
    )
    birth_today = (
        User.objects.filter(birthday__month=cur_date_month)
        .filter(birthday__day=cur_date_day)
        .values("email", "pk")
    )
    return {"birth_today": birth_today}
