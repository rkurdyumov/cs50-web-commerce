from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm

def index(request):
  listings = Listing.objects.filter(active=True)
  if "category" in request.GET:
    listings = listings.filter(category=request.GET["category"])
  if "owner" in request.GET:
    owner_id = User.objects.filter(username=request.GET["owner"]).first()
    listings = listings.filter(owner=owner_id)
  return render(request, "auctions/index.html", {
    "listings": listings,
  })

def categories(request):
  categories = Listing.objects.values_list("category", flat=True)
  return render(request, "auctions/categories.html", {
    "categories": [c for c in categories if c]
  })

@login_required
def watchlist(request):
  return render(request, "auctions/watchlist.html", {
    "listings": Listing.objects.filter(watchers=request.user)
  })

def listing(request, listing_id):
  listing = Listing.objects.get(pk=listing_id)

  if request.method == "POST":

    if request.POST.get("bid"):
      bid_form = BidForm(request.POST, instance=Bid(listing=listing, user=request.user))
      if bid_form.is_valid():
        bid_form.save()
        messages.success(request, "Bid submission successful")
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        bid_form = BidForm()

    if request.POST.get("watch"):
      if request.POST.get("watch") == "watch":
        listing.watchers.add(request.user)
      if request.POST.get("watch") == "unwatch":
        listing.watchers.remove(request.user)
      return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    if request.POST.get("close"):
      listing.active = False
      listing.save()
      return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    if request.POST.get("comment"):
      comment_form = CommentForm(request.POST, instance=Comment(listing=listing, user=request.user))
      if comment_form.is_valid():
        comment_form.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
      comment_form = CommentForm()

  else:
    bid_form = BidForm()
    comment_form = CommentForm()

  return render(request, "auctions/listing.html", {
    "listing": listing,
    "watched": request.user in listing.watchers.all(),
    "comments": listing.listing_comments.all(),
    "bid_form": bid_form,
    "comment_form": comment_form
  })

@login_required
def create(request):
  if request.method == "POST":
    form = ListingForm(request.POST)
    if form.is_valid():
      new_listing = form.save(commit=False)
      new_listing.owner = request.user
      new_listing.save()
      messages.success(request, "Listing submission successful")
      return HttpResponseRedirect(reverse("listing", args=[new_listing.id]))
  else:
    form = ListingForm()
  return render(request, "auctions/create.html", {
    "form": form
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

@login_required
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