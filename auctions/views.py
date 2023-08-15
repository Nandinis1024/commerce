from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import urllib

from .models import User
from .models import Listing
from .models import Category
from .models import Watchlist
from .models import Comments
from .models import Bid


def index(request):
    items = Listing.objects.filter(is_active=True)
    categories = Category.objects.all()

    return render(request, "auctions/index.html",{"items": items, "categories": categories})


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
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        created_by = request.user

        category_added, created = Category.objects.get_or_create(category_name=category)

        bid_added = Bid(bid=price, bid_id=request.user)
        bid_added.save()
        

        listing = Listing(title=title, description=description, image=image, price=bid_added, category=category_added, created_by=created_by)
        listing.save()   
        items = Listing.objects.all()
        return HttpResponseRedirect(reverse("index"))
     
    return render(request, "auctions/create.html")


def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    comment_items = Comments.objects.filter(item_id=listing_data)
    isowner = request.user.username == listing_data.created_by.username
    return render(request, "auctions/listing.html",{"listing_data": listing_data, "comment_items": comment_items, "isowner": isowner})


def category(request):
    if request.method == "POST":

        category_chosen = request.POST["category_chosen"]
        cat = Category.objects.get(category_name=category_chosen)
        items = Listing.objects.filter(category=cat)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{"items": items, "categories": categories})

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(Listing, id=listing_id)
        watchlist_item, created = Watchlist.objects.get_or_create(user_id=request.user, listing_id=listing)
        watchlist_items = Watchlist.objects.filter(user_id=request.user)
        return render(request, "auctions/watchlist.html", {'watchlist_items': watchlist_items}) 
    watchlist_items = Watchlist.objects.filter(user_id=request.user)       
    return render(request, "auctions/watchlist.html", {'watchlist_items': watchlist_items})    
        
def delete(request, listing_id):
    watchlist_item = get_object_or_404(Watchlist, user_id=request.user, listing_id=listing_id)
    watchlist_item.delete()
    return redirect('watchlist')
   

def comments(request):
    if request.method == 'POST':
        item_id = request.POST["listing_id"]
        item = get_object_or_404(Listing, id=item_id)
        comments = request.POST["comments"]
        comment, created = Comments.objects.get_or_create(comment_id=request.user, item_id=item, comment=comments)
        return redirect("listing", id=item_id)
    comment_items = Comments.objects.all() 
    return render(request, 'listing.html', {'comment_items': comment_items})    

def add_bid(request):
    if request.method == 'POST':
        item_id = request.POST["listing_id"]
        new_bid = request.POST["new_bid"]
        listing = get_object_or_404(Listing, id=item_id)
        old_bid = listing.price.bid
        if int(new_bid) > old_bid:
            update_bid = Bid(bid=new_bid, bid_id=request.user)
            update_bid.save()
            listing.price = update_bid
            listing.save()
            messages.success(request, "Bid added successfully")
            return redirect("listing", id=item_id) 
        else:
            messages.error(request, "Bid failed!",extra_tags='danger')
            return redirect("listing", id=item_id)                       
    return render(request, 'listing.html', {"listing_data": listing})       

def close_bid(request):
    if request.method == 'POST':

        item_id = request.POST["listing_id"]
        listing = get_object_or_404(Listing, id=item_id)
        listing.is_active = False
        listing.save()
        return redirect('index')
    return render(request, 'listing.html', {"listing_data": listing})         