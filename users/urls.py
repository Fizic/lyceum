from django.urls import path

from . import views

app_name = 'urls'
urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]
