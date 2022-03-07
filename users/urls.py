from django.urls import path

from . import views

urlpatterns = [
    path('getUserInfo/', views.getUserInfo),
    path('signin/',views.signin),
    path('register/',views.register),
    path('logout/',views.logout),
]