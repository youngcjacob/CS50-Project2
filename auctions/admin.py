from django.contrib import admin

from auctions.models import Auction_listings, Bids, Comments

# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Comments)
admin.site.register(Bids)
