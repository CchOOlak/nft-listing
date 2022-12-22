from django.db import models
from api.models import Buyer, Seller

# class NFT(models.Model):
#     name = models.CharField(max_length=500, null=False)
#     description = models.TextField(default="", blank=True)


class NFTListing(models.Model):
    # nft = models.ForeignKey(NFT, related_name='listing', on_delete=models.CASCADE)
    nft = models.CharField(max_length=250, null=False)
    seller = models.ForeignKey(
        Seller, related_name='listings', on_delete=models.CASCADE)
    fixed_price = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)


class NFTOffer(models.Model):
    listing = models.ForeignKey(
        NFTListing, related_name='offers', on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Buyer, related_name='offers', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    status_enum = (
        (0, 'pending'),
        (1, 'rejected'),
        (2, 'accepted'),
    )
    status = models.IntegerField(choices=status_enum, default=0)

    def save(self, *args, **kwargs):
        if self.status == 2:
            for offer in self.listing.offers.all():
                # reject other offers of this listing
                offer.status = 1
                offer.save()
        return super().save(*args, **kwargs)
