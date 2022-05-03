from django.urls import path

from . import views

urlpatterns = [
    path('getProductById/', views.getProductById),
    path('createNewProduct/',views.createNewProduct),
    path('getAllProducts/',views.getAllProducts),
]