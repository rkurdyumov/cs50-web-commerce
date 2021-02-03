from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ModelForm, Textarea, TextInput

class User(AbstractUser):
  pass

class Listing(models.Model):
  title = models.CharField(max_length=64)
  description = models.TextField()
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_listings")
  start_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  active = models.BooleanField(default=True)
  image = models.URLField(blank=True)
  category = models.CharField(max_length=64, blank=True)
  watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

  def price(self):
    try:
     max_bid = self.listing_bids.latest("price").price
    except Bid.DoesNotExist:
      max_bid = -1
    return max(self.start_bid, max_bid)

  def winner(self):
    try:
      winner = self.listing_bids.latest("price").user
    except Bid.DoesNotExist:
      winner = None
    return winner

  def __str__(self):
    return f"{self.title}"

class Bid(models.Model):
  price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_bids")
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user} bid {self.price} on {self.listing} at {self.timestamp}"

class Comment(models.Model):
  text = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")

  def __str__(self):
    return f"{self.user} commented on {self.listing}: {self.text}"