from django.contrib.auth.backends import BaseBackend, UserModel, ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

from rating.models import Rating
from users.forms import UserForm
from users.models import ExtendedUser
from django.contrib.auth import get_user_model

User = get_user_model()


def get_profile_data(request) -> dict:
    user = User.objects.filter(username=request.user.username).only('email', 'first_name',
                                                                    'last_name').prefetch_related(
        Prefetch('rating', queryset=Rating.objects.filter(star=5).only('item').select_related('item'))).first()
    user_form = UserForm(instance=request.user)
    context = {
        'user': user,
        'user_form': user_form
    }
    return context


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = ExtendedUser.objects.get(email=username)
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
