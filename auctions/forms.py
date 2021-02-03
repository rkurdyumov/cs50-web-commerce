from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, TextInput

from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ["title", "description", "start_bid", "image", "category"]
    labels = {
      "image": "Image URL"
    }
    widgets = {
      "title": TextInput(attrs={"size": 30}),
      "description": Textarea(attrs={"rows": 4, "cols": 30}),
      "start_bid": TextInput(attrs={"size": 6})
    }

class BidForm(ModelForm):
  class Meta:
    model = Bid
    fields = ["price"]
    labels = {
      "price": "Enter bid"
    }
    widgets = {
      "price": TextInput(attrs={"size": 6})
    }

  def clean_price(self):
    price = self.cleaned_data.get("price")
    if price <= self.instance.listing.price():
      raise ValidationError("Bid must be greater than current price!")
    return price

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ["text"]
    labels = {
      "text": "Enter comment"
    }
    widgets = {
      "text": Textarea(attrs={"rows": 4, "cols": 30})
    }