from django.urls import path

from api import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),

    path('nft/listings/add/', views.add_listing, name='add_listing'),
    path('nft/listings/', views.get_listings, name='get_listings'),
    path('nft/offers/', views.get_offers, name='get_offers'),
    path('nft/offers/add', views.add_offer, name='add_offer'),
    path('nft/offers/<int:offer_id>/',
         views.determine_offer, name='determine_offer'),
]
