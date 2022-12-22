from django.urls import path

from api import views

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/login/', views.login),

    path('nft/listings/add/', views.add_listing),
    path('nft/listings/', views.get_listings),
    path('nft/offers/', views.get_offers),
    path('nft/offers/add', views.add_offer),
    path('nft/offers/<int:offer_id>/', views.determine_offer),
]
