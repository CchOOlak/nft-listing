from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
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
            "message": "wrong input",
        }, HTTP_400_BAD_REQUEST)
    listing = NFTListing()
    listing.nft = nft
    listing.seller = request.user.seller.all()[0]
    listing.fixed_price = fixed_price
    listing.view_count = view_count
    listing.save()

    return Response({
        "message": "listing created successfully"
    }, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsSeller | IsBuyer,))
def get_listings(request):
    # fixed_price, -fixed_price, views, -view_count
    ordering = request.GET.get('ordering', 'id')
    queryset = NFTListing.objects.all().order_by(ordering)
    serialized_data = NFTListingSerializer(queryset, many=True).data
    return Response(serialized_data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsBuyer,))
def get_offers(request):
    buyer = request.user.buyer.all()[0]
    queryset = buyer.offers.all()
    serialized_data = NFTOfferSerializer(queryset, many=True).data
    return Response(serialized_data, HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsBuyer,))
def add_offer(request):
    listing_id = request.data.get("listing_id", None)
    price = request.data.get("price", None)
    if listing_id is None or price is None:
        return Response({
            "message": "wrong input",
        }, HTTP_400_BAD_REQUEST)
    try:
        listing = NFTListing.objects.get(pk=listing_id)
    except:
        return Response({
            "message": "listing not found",
        }, HTTP_404_NOT_FOUND)
    offer = NFTOffer()
    offer.listing = listing
    offer.buyer = request.user.buyer.all()[0]
    offer.price = price
    offer.save()
    return Response({
        "message": "offer created successfully",
    }, HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsSeller,))
def determine_offer(request, offer_id):
    status = request.data.get("status", None)
    if status is None or not (status == 1 or status == 2):
        return Response({
            "message": "wrong input",
        }, HTTP_400_BAD_REQUEST)
    try:
        offer = NFTOffer.objects.get(pk=offer_id)
    except:
        return Response({
            "message": "offer not found",
        }, HTTP_404_NOT_FOUND)
    offer.status = status
    offer.save()
    return Response({
        "message": "offer determined successfully"
    }, HTTP_200_OK)
