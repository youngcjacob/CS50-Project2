import email
from http.server import HTTPServer
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .models import Auction_listing, User, Comment, Bid, Watchlist


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    starting_bid = forms.IntegerField(label="Bid")
    url_image = forms.URLField(label="Image URL")
    category = forms.CharField(label="Category")
    #listing_creator = forms.CharField(label="Username")


def index(request):
    listings = Auction_listing.objects.all()
    listings = listings.filter(listing_status=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html",
                      {"form": NewListingForm()})
    elif request.method == "POST":
        listing = NewListingForm(request.POST)
        try:
            if listing.is_valid():
                user = request.user
                title = listing.cleaned_data['title']
                description = listing.cleaned_data['description']
                bid = listing.cleaned_data['starting_bid']
                url_image = listing.cleaned_data['url_image']
                category = listing.cleaned_data['category']
                # creator = user.id   listing.cleaned_data['listing_creator']
                a = Auction_listing(
                    title=title,
                    description=description,
                    starting_bid=bid,
                    url_image=url_image,
                    category=category,
                    listing_creator=user
                )
                a.save()
                return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "auctions/create.html",
                          {"message": "Duplicate title, please create a new listing"})


def add_watchlist(request):

    return render(request, "auctions/watchlist.html")


def categories(request):
    return render(request, "auctions/categories.html")


def listing(request, listing_title):
    # filter to the title of the listing and the current user
    listing = Auction_listing.objects.get(id=listing_title)
    try:
        watchlist = Watchlist.objects.get(
            auction_listing=listing_title, user=request.user)
    except:
        watchlist = None
    try:
        comments = Comment.objects.all()
        comments = comments.filter(auction_listing=listing_title)
    except:
        comments = None
    return render(request, "auctions/listing.html",
                  {
                      "listing": listing,
                      "watchlist": watchlist,
                      "comments": comments
                  })


def add_comment(request):
    pass


def add_bid(request):
    pass


def closed(request):
    listings = Auction_listing.objects.all()
    listings = listings.filter(listing_status=False)
    return render(request, "auctions/closed.html", {
        "listings": listings
    })
