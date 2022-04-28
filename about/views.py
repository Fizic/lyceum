from django.shortcuts import render


def description(request):
    template = "about/description.html"
    context = {}
    return render(request, template, context)
