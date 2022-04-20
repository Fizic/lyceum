from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import pbkdf2
from django.views import View
from django.utils.decorators import method_decorator

from users.forms import ProfileForm, EmailAuthentication
from users.models import UserWithBirthday
from users.services import get_profile_data


def user_list(request):
    template = "users/user_list.html"
    users = User.objects.all()
    context = {"users": users}
    return render(request, template, context)


def user_detail(request, pk: int):
    template = "users/user_detail.html"
    user = User.objects.get(id=pk)
    ratings = user.rating.filter(star=5).select_related("item").only("item__name")
    context = {"user": user, "ratings": ratings}
    return render(request, template, context)


class LoginView(View):
    def get(self, request):
        template = "users/login.html"
        context = {"form": EmailAuthentication()}
        return render(request, template, context)

    def post(self, request):
        form = EmailAuthentication(request.POST)
        if not form.is_valid():
            template = "users/login.html"
            context = {"form": EmailAuthentication(), "errors": form.errors}
            return render(request, template, context)
        try:
            user = UserWithBirthday.objects.get(authentication_email=form.cleaned_data["email"])
        except ObjectDoesNotExist:
            return HttpResponse('123')


class SignUp(View):
    def get(self, request):
        template = "users/signup.html"
        context = {"form": UserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            template = "users/signup.html"
            context = {"form": UserCreationForm(), "errors": form.errors}
            return render(request, template, context)

        form.save()
        return redirect("users:login")


@method_decorator(login_required, name='get')
class Profile(View):
    def get(self, request):
        template = "users/profile.html"
        context = get_profile_data(request)
        return render(request, template, context)

    def post(self, request):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            template = "users/profile.html"
            context = get_profile_data(request)
            context['errors'] = form.errors
            return render(request, template, context)

        user = request.user
        if form.cleaned_data["authentication_email"]:
            user.authentication_email = form.cleaned_data["authentication_email"]
        if form.cleaned_data["first_name"]:
            user.first_name = form.cleaned_data["first_name"]
        user.save()

        if form.cleaned_data["birth_day"]:
            user_with_birthday = UserWithBirthday.objects.get_or_create(user=user)[0]
            user_with_birthday.birthday = form.cleaned_data["birth_day"]
            user_with_birthday.save()

        return redirect('users:profile')
