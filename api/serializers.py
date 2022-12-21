from rest_framework import serializers

from api.models import *


class NFTListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTListing
        exclude = []