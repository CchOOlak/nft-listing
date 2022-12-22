import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.models import *
from api.serializers import *


class GetListingsTest(TestCase):
    def setUp(self):
        self.client = Client()

        user1 = User.objects.create_user("user1", "user1@gmail.com", "1234")
        seller1 = Seller.objects.create(user=user1)
        user2 = User.objects.create_user("user2", "user2@gmail.com", "1234")
        seller2 = Seller.objects.create(user=user2)
        user3 = User.objects.create_user("user3", "user3@gmail.com", "1234")
        Buyer.objects.create(user=user3)

        self.buyer_token, _ = Token.objects.get_or_create(user=user3)
        self.seller_token, _ = Token.objects.get_or_create(user=user1)

        NFTListing.objects.create(
            nft="nft1", seller=seller1, fixed_price=1000, view_count=100
        )
        NFTListing.objects.create(
            nft="nft2", seller=seller1, fixed_price=1200, view_count=120
        )
        NFTListing.objects.create(
            nft="nft3", seller=seller2, fixed_price=1100, view_count=110
        )
        NFTListing.objects.create(
            nft="nft4", seller=seller2, fixed_price=1300, view_count=130
        )

    def test_get_listings_no_order(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer_token.key}'}
        response = self.client.get(reverse('get_listings'), {}, **header)

        listings = NFTListing.objects.all().order_by('id')
        serialized = NFTListingSerializer(listings, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized)

    def test_get_listings_fixed_price_order(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer_token.key}'}
        response = self.client.get(
            reverse('get_listings'), {}, **header, QUERY_STRING='ordering=-fixed_price')

        listings = NFTListing.objects.all().order_by('-fixed_price')
        serialized = NFTListingSerializer(listings, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized)


class AddListingTest(TestCase):
    def setUp(self):
        self.client = Client()

        user1 = User.objects.create_user("user1", "user1@gmail.com", "1234")
        Seller.objects.create(user=user1)
        user2 = User.objects.create_user("user2", "user2@gmail.com", "1234")
        Buyer.objects.create(user=user2)

        self.buyer_token, _ = Token.objects.get_or_create(user=user2)
        self.seller_token, _ = Token.objects.get_or_create(user=user1)

        self.payload = {
            "nft": "hello man",
            "fixed_price": 1000,
            "view_count": 120,
        }

    def test_add_listing_seller(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.seller_token.key}'}
        response = self.client.post(
            reverse('add_listing'), json.dumps(self.payload), 'application/json', **header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_listing_buyer(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer_token.key}'}
        response = self.client.post(
            reverse('add_listing'), json.dumps(self.payload), 'application/json', **header)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AddOfferTest(TestCase):
    def setUp(self):
        self.client = Client()

        user1 = User.objects.create_user("user1", "user1@gmail.com", "1234")
        seller1 = Seller.objects.create(user=user1)
        user2 = User.objects.create_user("user2", "user2@gmail.com", "1234")
        self.buyer1 = Buyer.objects.create(user=user2)
        user3 = User.objects.create_user("user3", "user3@gmail.com", "1234")
        self.buyer2 = Buyer.objects.create(user=user3)

        self.seller_token, _ = Token.objects.get_or_create(user=user1)
        self.buyer1_token, _ = Token.objects.get_or_create(user=user2)
        self.buyer2_token, _ = Token.objects.get_or_create(user=user3)

        listing1 = NFTListing.objects.create(
            nft="nft1", seller=seller1, fixed_price=1000, view_count=100
        )
        listing2 = NFTListing.objects.create(
            nft="nft2", seller=seller1, fixed_price=1200, view_count=120
        )

        offer1 = NFTOffer.objects.create(
            listing=listing1, price=1100, buyer=self.buyer1
        )
        NFTOffer.objects.create(
            listing=listing2, price=1300, buyer=self.buyer1
        )

        self.offer_id = offer1.id

        self.add_payload = {
            "listing_id": listing1.id,
            "price": 1400,
        }
        self.accept_payload = {
            "status": 2,
        }

    def test_get_offers(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer1_token.key}'}
        response = self.client.get(reverse('get_offers'), {}, **header)

        offers = self.buyer1.offers.all()
        serialized = NFTOfferSerializer(offers, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized)

    def test_add_offer(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer2_token.key}'}
        response = self.client.post(
            reverse('add_offer'), self.add_payload, **header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_offer(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.seller_token.key}'}
        response = self.client.post(
            reverse('determine_offer', kwargs={"offer_id": self.offer_id}), self.accept_payload, **header)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_accept_offer_permission_denied(self):
        header = {'HTTP_AUTHORIZATION': f'Token {self.buyer1_token.key}'}
        response = self.client.post(
            reverse('determine_offer', kwargs={"offer_id": self.offer_id}), self.accept_payload, **header)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)