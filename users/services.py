from django.contrib.auth.backends import BaseBackend, UserModel, ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from users.forms import ProfileForm
from users.models import UserWithBirthday


def get_profile_data(request) -> dict:
    user = request.user
    ratings = user.rating.filter(star=5).select_related("item").only("item__name")
    form = ProfileForm()
    context = {"user": user, "ratings": ratings, "form": form}
    return context


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user_with_birthday = UserWithBirthday.objects.get(authentication_email=username)
            user = User.objects.get(extend_user=user_with_birthday)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
