from django.contrib import admin

from .models import Listing, Bid, Comment, User

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "active")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)