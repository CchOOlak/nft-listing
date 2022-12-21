from django.urls import path

from api import views

urlpatterns = [
     path('hello_world/', views.helloworld),

     path('auth/register/', views.register),
     path('auth/login/', views.login),

     path('nft/add/', views.add_listing),
     path('nft/listings/', views.get_listings),
]
