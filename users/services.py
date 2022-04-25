from django.contrib.auth.backends import BaseBackend, UserModel, ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from users.forms import ProfileForm
from users.models import ExtendedUser
from django.contrib.auth import get_user_model

User = get_user_model()


def get_profile_data(request) -> dict:
    user = request.user
    ratings = user.rating.filter(star=5).select_related("item").only("item__name")
    form = ProfileForm()
    context = {"user": user, "ratings": ratings, "form": form}
    return context


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = ExtendedUser.objects.get(email=email)
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
