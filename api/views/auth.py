from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from api.models import Seller, Buyer


@csrf_exempt
@api_view(["POST"])
def register(request):
    username = request.data.get("username", None)
    email = request.data.get("email", None)
    password = request.data.get("password", None)
    is_seller = request.data.get("is_seller", False)
    if username is None or password is None:
        return Response({'message': 'provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(username, email, password)
        if is_seller:
            Seller.objects.create(user=user)
        else:
            Buyer.objects.create(user=user)
        message = "user registered successfully"
    except:
        message = "user already exists"
    user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'message': message,
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def login(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    if username is None or password is None:
        return Response({'message': 'provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({
            'message': 'username or password is wrong',
        }, status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'message': 'login successfully',
    }, status=HTTP_200_OK)
