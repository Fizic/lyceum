from django.urls import path

from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
]
