from rest_framework import serializers

from api.models import *


class NFTListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTListing
        exclude = []


class NFTOfferSerializer(serializers.ModelSerializer):
    listing = NFTListingSerializer(many=False, read_only=True)

    class Meta:
        model = NFTOffer
        fields = ['id', 'listing', 'buyer', 'price', 'status']
