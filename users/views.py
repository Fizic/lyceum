from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from users.forms import ProfileForm, EmailAuthentication, CustomUserCreationForm
from users.models import ExtendedUser
from users.services import get_profile_data

User = get_user_model()


class UserListView(View):
    def get(self, request):
        template = "users/user_list.html"
        users = User.objects.all()
        context = {"users": users}
        return render(request, template, context)


class UserDetailView(View):
    def get(self, request, pk: int):
        template = "users/user_detail.html"
        user = User.objects.get(id=pk)
        ratings = user.rating.filter(star=5).select_related("item").only("item__name")
        context = {"user": user, "ratings": ratings}
        return render(request, template, context)


class SignUpView(View):
    def get(self, request):
        template = "users/signup.html"
        context = {"form": CustomUserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if not form.is_valid():
            template = "users/signup.html"
            context = {"form": UserCreationForm(), "errors": form.errors}
            return render(request, template, context)

        form.save()
        return redirect("users:login")


class LoginView(View):
    def get(self, request):
        template = "users/login.html"
        form = EmailAuthentication()
        context = {"form": form}
        return render(request, template, context)

    def post(self, request):
        form = EmailAuthentication(request.POST)
        if not form.is_valid():
            template = "users/login.html"
            form = EmailAuthentication()
            context = {"from": form, "errors": form.errors}
            return render(request, template, context)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("users:profile")

        template = "users/login.html"
        form = EmailAuthentication()
        context = {"from": form, "errors": ["Неверный пароль или email"]}
        return render(request, template, context)


@method_decorator(login_required, name="get")
class ProfileView(View):
    def get(self, request):
        template = "users/profile.html"
        context = get_profile_data(request)
        return render(request, template, context)

    def post(self, request):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            template = "users/profile.html"
            context = get_profile_data(request)
            context["errors"] = form.errors
            return render(request, template, context)

        user = request.user
        if form.cleaned_data["authentication_email"]:
            user.authentication_email = form.cleaned_data["authentication_email"]
        if form.cleaned_data["first_name"]:
            user.first_name = form.cleaned_data["first_name"]
        user.save()

        if form.cleaned_data["birth_day"]:
            user_with_birthday = ExtendedUser.objects.get_or_create(user=user)[0]
            user_with_birthday.birthday = form.cleaned_data["birth_day"]
            user_with_birthday.save()

        return redirect("users:profile")
