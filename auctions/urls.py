from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("category/", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("delete/<int:listing_id>", views.delete, name="delete"),
    path("comments/", views.comments, name="comments"),
    path("add_bid/", views.add_bid, name="add_bid"),
    path("close_bid/", views.close_bid, name="close_bid")
    


]
