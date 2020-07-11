from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django import forms
from .models import User, Listing, Bid, Comment, Watch

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'created_on', 'post', 'active']

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
    closed = Listing.objects.filter(active=False)
    return render(request, "auctions/index.html", {
        "active": active,
        "closed": closed,
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

@login_required
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

@login_required
def add_watch(request, item):
    itemforsale = Listing.objects.filter(title=item).first()
    Watch(user=request.user, item=itemforsale).save()
    
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def remove_watch(request, item):
    itemforsale = Listing.objects.filter(title=item).first()
    watchlist = Watch.objects.filter(user=request.user, item=itemforsale.id).first()
    watchlist.delete()   
    
    return HttpResponseRedirect(reverse("watchlist"))
        
@login_required
def watch(request):
    watchlist = Watch.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "wlist": watchlist,
        "user": request.user
    })


def listing(request, item):
    itemforsale = Listing.objects.filter(title=item).first()
    comments = Comment.objects.filter(post=itemforsale.id)
    highbid = Bid.objects.filter(item=itemforsale.id).first()
    watchlist = Watch.objects.filter(user=request.user, item=itemforsale.id).first()   

    if itemforsale == None:
        return render(request, "auctions/error.html")            
   
    return render(request, "auctions/listing.html", {
            "item": itemforsale,
            "highbid": highbid,
            "startbid": itemforsale.start_bid,
            "form": BidForm,
            "commform": CommentForm,
            "comments": comments,
            "user": request.user,
            "watchlist": watchlist
        })

@login_required
def comment(request, item):
    c = CommentForm(request.POST)
    itemforsale = Listing.objects.filter(title=item).first()
    if c.is_valid():
        comm = c.save(commit=False)
        comm.post = itemforsale
        comm.user = request.user
        comm.save()
        return HttpResponseRedirect(reverse("listing", args=[item]))

    else:
        return render(request, "auctions/error.html")

def category(request):
    return render(request, "auctions/category.html", {
    })

@login_required
def bid(request, item):
    itemforsale = Listing.objects.filter(title=item).first()
    highbid = Bid.objects.filter(item=itemforsale.id).first()

    b = BidForm(request.POST)

    if highbid == None:
        cbid = itemforsale.start_bid
    else:
        cbid = highbid.value

    if b.is_valid():
        bid = b.save(commit=False)
        bid.item = itemforsale
        bid.user = request.user
        if bid.value <= cbid:
            return render(request, "auctions/error.html")
        else:
            bid.save()                     
            return HttpResponseRedirect(reverse("listing", args=[item]))
    else:
        return render(request, "auctions/error.html")


@login_required
def end(request, item):

    itemclose = Listing.objects.filter(title=item).first()
    itemclose.active = False
    itemclose.save(update_fields=['active'])

    return HttpResponseRedirect(reverse("listing", args=[item]))
    