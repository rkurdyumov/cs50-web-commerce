from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("categories", views.categories, name="categories"),
  path("watchlist", views.watchlist, name="watchlist"),
  path("listings", views.index, name="listings"),
  path("listings/<int:listing_id>", views.listing, name="listing"),
  path("listings/new", views.create, name="create"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register")
]
