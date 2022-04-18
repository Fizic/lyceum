from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from users.forms import ProfileForm
from users.models import UserWithBirthday


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


class SignUp(View):
    def get(self, request):
        template = "users/signup.html"
        context = {"form": UserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Форма заполнена не правильно")

        form.save()
        return redirect("users:login")


@method_decorator(login_required, name='get')
class Profile(View):
    def get(self, request):
        template = "users/profile.html"
        user = request.user
        ratings = user.rating.filter(star=5).select_related("item").only("item__name")
        form = ProfileForm()
        context = {"user": user, "ratings": ratings, "form": form}
        return render(request, template, context)

    def post(self, request):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Форма заполнена не правильно")

        user = request.user
        if form.cleaned_data["email"]:
            user.email = form.cleaned_data["email"]
        if form.cleaned_data["first_name"]:
            user.first_name = form.cleaned_data["first_name"]
        user.save()

        if form.cleaned_data["birth_day"]:
            user_with_birthday = UserWithBirthday.objects.get_or_create(user=user)[0]
            user_with_birthday.birthday = form.cleaned_data["birth_day"]
            user_with_birthday.save()

        return redirect('users:profile')
