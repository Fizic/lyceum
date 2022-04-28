from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from rating.models import Rating
from users.forms import BeautifulUserCreationForm, BeautifulAuthenticationForm, UserForm
from users.models import ExtendedUser
from users.services import get_profile_data

User = get_user_model()


class UserListView(View):
    def get(self, request):
        template = "users/user_list.html"
        users = User.objects.only("username")
        context = {"user": request.user, "users": users}
        return render(request, template, context)


class UserDetailView(View):
    def get(self, request, pk: int):
        template = "users/user_detail.html"
        detailed_user = (
            User.objects.filter(pk=pk)
            .only("email", "first_name", "last_name")
            .prefetch_related(
                Prefetch(
                    "rating",
                    queryset=Rating.objects.filter(star=5)
                    .only("item")
                    .select_related("item"),
                )
            )
            .first()
        )
        context = {"pk": pk, "user": request.user, "detailed_user": detailed_user}
        return render(request, template, context)


class SignUpView(View):
    def get(self, request):
        template = "users/signup.html"
        context = {"form": BeautifulUserCreationForm()}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")


class LoginView(View):
    def get(self, request):
        template = "users/login.html"
        form = BeautifulAuthenticationForm()
        context = {"form": form, "user": request.user}
        return render(request, template, context)

    def post(self, request):
        form = BeautifulAuthenticationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
        return self.get(request)


@method_decorator(login_required, name="get")
class ProfileView(View):
    def get(self, request):
        template = "users/profile.html"
        context = get_profile_data(request)
        return render(request, template, context)

    def post(self, request):
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data["email"]
            user.username = form.cleaned_data["username"]
            user.birthday = form.cleaned_data["birthday"]
            user.save()
            return redirect("profile")
        else:
            return self.get(request)
