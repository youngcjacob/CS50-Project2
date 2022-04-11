from tkinter import CASCADE
from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import modelformset_factory


class User(AbstractUser):
    pass


class Auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    url_image = models.ImageField()

    def __str__(self):
        return f"Check out this listing of a {self.title}. It has the following features: {self.description}."


class Bids(models.Model):
    bids = models.ForeignKey(
        Auction_listings, on_delete=models.CASCADE, related_name="bids")
    # want to have a two column table. First column is the listing title, second is the bid
    pass


class Comments(models.Model):
    pass
