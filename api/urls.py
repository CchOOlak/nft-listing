from django.urls import path

from api import views

urlpatterns = [
     path('hello_world/', views.helloworld),
     path('auth/register/', views.register),
     path('auth/login/', views.login),
]
