from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django import forms
from .models import User, Listing, Bid, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['current_bid', 'user', 'active']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['item', 'user', 'created_on']


def index(request):
    active = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active": active,
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


def sell(request):
    f = ListingForm(request.POST or None)
    if f.is_valid():
        item = f.save(commit=False)
        item.title = item.title.lower()
        item.user = request.user
        item.save()
        
        return HttpResponseRedirect(reverse("listing", args=[item.title]))
    
    return render(request, "auctions/sell.html", {
        "form": f 
        })

def watchlist(request):
    
    return render(request, "auctions/watchlist.html")

def listing(request, item):
    itemforsale = Listing.objects.filter(title=item).first()
    if itemforsale == None:
        return render(request, "auctions/error.html")
    
    b = BidForm(request.POST or None)
    if itemforsale.current_bid == None:
        cbid = itemforsale.start_bid
    else:
        cbid = itemforsale.current_bid
        
    if b.is_valid():
        bid = b.save(commit=False)
        bid.title = item
        bid.user = request.user
        if bid.value <= cbid:
            return render(request, "auctions/error.html")
        else:
            bid.save()
            itemforsale.current_bid = bid.value
            return render(request, "auctions/listing.html", {
            "item": itemforsale,
            "form": b
        })

    return render(request, "auctions/listing.html", {
            "item": itemforsale,
            "form": b
        })


    

    