from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def description(request):
    return HttpResponse('О проекте')
