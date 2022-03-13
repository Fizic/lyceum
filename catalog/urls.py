from django.urls import path

from .views import *

urlpatterns = [
    path('', item_list),
    path('<int:pk>/', item_detail),
]
