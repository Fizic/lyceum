from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def user_list(request):
    return HttpResponse('Список пользователей')


def user_detail(request, pk: int):
    return HttpResponse('Информация о пользователе')


def signup(request):
    return HttpResponse('Регистрация')


def profile(request):
    return HttpResponse('Мой профиль')
