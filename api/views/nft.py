from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
)

from api.models import *
from api.serializers import *


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsSeller,))
def add_listing(request):
    nft = request.data.get("nft", None)
    fixed_price = request.data.get("fixed_price", None)
    view_count = request.data.get("view_count", 0)
    if nft is None or fixed_price is None:
        return Response({
            "error": "wrong input",
        }, HTTP_400_BAD_REQUEST)
    listing = NFTListing()
    listing.nft = nft
    listing.seller = request.user.seller.all()[0]
    listing.fixed_price = fixed_price
    listing.view_count = view_count
    listing.save()

    return Response("listing created", status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsSeller|IsBuyer,))
def get_listings(request):
    ordering = request.GET.get('ordering', 'id')
    queryset = NFTListing.objects.all().order_by(ordering)
    serialized_data = NFTListingSerializer(queryset, many=True).data
    return Response(serialized_data, HTTP_200_OK)
