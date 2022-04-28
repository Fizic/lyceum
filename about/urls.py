from django.urls import path

from . import views

urlpatterns = [
    path('', views.DescriptionView.as_view(), name='description'),
]
