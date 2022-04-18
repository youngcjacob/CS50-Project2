from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("closed", views.closed, name="closing"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_bid", views.add_bid, name="add_bid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("Listing_<str:listing_title>", views.listing, name="listing")

]
