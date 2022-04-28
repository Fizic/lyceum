from django.shortcuts import render
from django.views import View


class DescriptionView(View):
    def get(self, request):
        template = "about/description.html"
        context = {
            'user': request.user
        }
        return render(request, template, context)
