from http.server import HTTPServer
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Auction_listings, User


def index(request):
    listings = Auction_listings.objects.all()
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
    return render(request, "auctions/create.html")
    # Will want to return to the all listings page when submitting


def submit_listing(request):
    listing_details = request.POST.getlist(listing)
    listing = Auction_listings(
        title=listing_details.Title,
        description=listing_details.Description,
        starting_bid=listing_details.Bid,
        url_image=listing_details.Image)
    listing.save()
    return redirect("auctions/index.html")
    # title = request.method  # add submission details for listing
    # # return the index page with the new listing at the top and all the other listings below

    # return render(request, "auctions/index.html", {
    #     "Title": title,
    #     "Description": description,
    #     "Starting_big": starting_bid,
    #     "Image": image
    # }
    # )


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def categories(request):
    return render(request, "auctions/categories.html")
