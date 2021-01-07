from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist
from . import util
from .forms import WatchListForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings":  [(entry, "{:.2f}".format(entry.starting_bid)) for entry in Listing.objects.all()]
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

@login_required(redirect_field_name="")
def createlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = None 
        category = None
        if "image" in request.POST:
            image = request.POST["image"]

        if "category" in request.POST:
            category = request.POST["category"]

        # try: 
        new_listing = Listing.objects.create(
            title=title, 
            description=description, 
            starting_bid=starting_bid,
            image=image,
            category=category
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
        # except:
            # ret
    else:
        return render(request, "auctions/createlisting.html")

def listing(request, listing):
    listing_id = Listing.objects.get(id=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing_id,
        "price": "{:.2f}".format(listing_id.starting_bid)
    })

@login_required(redirect_field_name="")
def watchlist(request):
    if request.method == "POST":
        current_user = request.user
        watchlist_item = Watchlist.objects.create(
            user = current_user,
            listing = Listing.objects.get(pk=request.POST["listing"])
        )
        watchlist_item.save()
        return render(request, "auctions/")