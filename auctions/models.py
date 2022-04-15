from tkinter import CASCADE
from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import modelformset_factory


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    url_image = models.URLField(blank=True)
    category = models.CharField(max_length=64)
    listing_status = models.BooleanField(default=True)
    listing_creator = models.ForeignKey(User,
                                        on_delete=models.CASCADE, related_name="listing_creator")
    highest_bidder = models.CharField(max_length=24, default="No Bids")

    def __str__(self):
        return f"Check out this listing of a {self.title}. It has the following features: {self.description}."


class Bid(models.Model):
    bid = models.IntegerField()
    auction_listing = models.ForeignKey(
        Auction_listing, on_delete=models.CASCADE, related_name="item_bid")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bid")

    def __str__(self):
        return f"{self.auction_listing.title} with a bid of: {self.bid}"


class Comment(models.Model):
    comment = models.CharField(max_length=64)
    auction_listing = models.ForeignKey(Auction_listing,
                                        on_delete=models.CASCADE, related_name="item_comment")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment")

    def __str__(self):
        return f"The {self.auction_listing.title}: {self.comment}"


class Watchlist(models.Model):
    auction_listing = models.ForeignKey(
        Auction_listing, on_delete=models.CASCADE, related_name="item_watchlist")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_watchlist")

    def __str__(self):
        return f"{self.user} has {self.auction_listing.title} on their watchlist"
