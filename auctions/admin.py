from django.contrib import admin

from auctions.models import Auction_listing, Bid, Comment, Watchlist, User

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
