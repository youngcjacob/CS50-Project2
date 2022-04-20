import email
from http.server import HTTPServer
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .models import Auction_listing, User, Comment, Bid, Watchlist, Category


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    starting_bid = forms.IntegerField(label="Bid")
    url_image = forms.URLField(label="Image URL")
    category = forms.CharField(label="Category")


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
                    listing_creator=user,
                    highest_bidder=user
                )
                a.save()
                listing_details = Auction_listing.objects.get(title=title)
                add_bid = Bid(
                    bid=bid, auction_listing=listing_details, user=user)
                add_bid.save()
                categories = Category.objects.all()

                if len(categories.filter(category=category)) == 0:
                    create_cat = Category(category=category)
                    create_cat.save()

                return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "auctions/error.html",
                          {"Message": "Duplicate title, please create a new listing"})


def add_watchlist(request):
    listing = Auction_listing.objects.get(id=request.POST['listing_id'])
    listing_id = request.POST['listing_id']
    bids = Bid.objects.all()
    bids = Bid.objects.filter(auction_listing=listing)
    current_bid = list(bids.values())[len(bids)-1]['bid']

    try:
        watchlist_add = request.POST["Add"]
        add_to_watchlist = Watchlist(
            auction_listing=listing, user=request.user)
        add_to_watchlist.save()
    except:
        watchlist_remove = request.POST["Remove"]
        remove_from_watchlist = Watchlist.objects.get(
            auction_listing=listing)
        remove_from_watchlist.delete()
    try:
        watchlist = Watchlist.objects.get(
            auction_listing=listing_id, user=request.user)
    except:
        watchlist = None
    try:
        comments = Comment.objects.all()
        comments = comments.filter(auction_listing=listing_id)
    except:
        comments = None
    return render(request, "auctions/listing.html",
                  {
                      "listing": listing,
                      "watchlist": watchlist,
                      "comments": comments,
                      "bid": current_bid
                  })


def categories(request):
    #listings = Auction_listing.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


def filtered_categories(request, category):
    all_listings = Auction_listing.objects.all()
    listings = all_listings.filter(category=category, listing_status=True)
    return render(request, "auctions/filtered_categories.html", {
        'listings': listings,
        'category': category
    })


def listing(request, listing_title):
    # filter to the title of the listing and the current user
    listing = Auction_listing.objects.get(id=listing_title)
    bids = Bid.objects.all()
    bids = Bid.objects.filter(auction_listing=listing)
    current_bid = list(bids.values())[len(bids)-1]['bid']
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
                      "comments": comments,
                      "bid": current_bid

                  })


def watchlist(request):
    watchlist_listings = Watchlist.objects.all()
    watchlist_listings = watchlist_listings.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {
        "listings": watchlist_listings
    })


def add_comment(request):
    listing_details = Auction_listing.objects.get(
        id=request.POST['listing_id'])
    comment = request.POST['comment']
    new_comment = Comment(
        comment=comment, auction_listing=listing_details, user=request.user)
    new_comment.save()

    return listing(request, listing_details.id)


def add_bid(request):
    bid_amount = int(request.POST['new_bid'])  # captured bid amount
    listing_item = request.POST['listing_id']  # captures item
    all_bids = Bid.objects.all()
    current_bid = all_bids.filter(
        auction_listing=listing_item)  # gets the correct object
    current_bid = list(current_bid.values())[
        0]['bid']  # provides a list of values
    if current_bid > bid_amount:
        return render(request, "auctions/error.html",
                      {"Message": "Please enter a value greater than the current bid"})
    else:
        add_bid = Bid(bid=bid_amount,
                      auction_listing=Auction_listing.objects.get(id=listing_item), user=request.user)
        add_bid.save()
        Auction_listing.objects.filter(id=listing_item).update(
            highest_bidder=request.user)
        return listing(request, listing_item)


def closed(request):
    listings = Auction_listing.objects.all()
    listings = listings.filter(listing_status=False)
    return render(request, "auctions/closed.html", {
        "listings": listings
    })


def close_listing(request):
    update_listing = Auction_listing.objects.filter(
        id=request.POST['listing_id']).update(listing_status=False)
    return listing(request, request.POST['listing_id'])
