from django.db import models
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class Seller(models.Model):
    user = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)


class Buyer(models.Model):
    user = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE)

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            return len(user.seller.all()) == 1
        return False

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            return len(user.buyer.all()) == 1
        return False