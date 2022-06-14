from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):

    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "watch_count": watch_count
    })


def categories(request):
    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "watch_count": watch_count
    })

@login_required
def display_category(request, category_type):
    category_list = []
    for l in Listing.objects.all():
        if category_type == l.category.category:
            category_list.append(l)

    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    return render(request, 'auctions/display_category.html', {
        "category_list": category_list,
        "category_type": category_type,
        "watch_count": watch_count
        })

@login_required
def add_watchlist(request, article_id):
    try:
        request.user.watchlist.get().products.add(article_id)
    except:
        watchlist = Watchlist.objects.create_watchlist(request.user)
        request.user.watchlist.get().products.add(article_id)
    
    return HttpResponseRedirect(reverse("index"))

@login_required
def remove_watchlist(request, article_id):
    request.user.watchlist.get().products.remove(article_id)
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    try:
        watchlist = request.user.watchlist.get().products.all()
    except:
        watchlist = Watchlist.objects.create_watchlist(request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "listings": Listing.objects.all(),
        "watch_count": watch_count
    })

@login_required
def create_listing(request):
    l = ListingForm(initial={'created_by': request.user})
    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    if request.method == "POST":
        name_article = request.POST["name_article"]
        price = request.POST["price"]
        description = request.POST["description"]
        category = request.POST["category"]
        created_by = request.user
        if "img" in request.FILES:
            img = request.FILES["img"]
        else:
            img = False

        l = ListingForm(request.POST, request.FILES)

        if l.is_valid():
            l.save()
            messages.success(request, f'"{name_article}" added!')
            l = ListingForm(initial={'created_by': request.user})

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all(),
        "form": l,
        "watch_count": watch_count
    })

@login_required
def remove_listing(request, remove_id):
    Listing.objects.filter(id=remove_id).delete()
    return HttpResponseRedirect(reverse("index"))

def close(request, article_id):
    closed_post = Listing.objects.get(pk=article_id)
    closed_post.is_active = False
    try:
        closed_post.winner = closed_post.bid_listing.last().bid_created_by_id
    except:
        closed_post.winner = None
    closed_post.save()
    return HttpResponseRedirect(reverse("closed_auctions"))

def closed_auctions(request):
    user_won = request.user.won.all()
    user_closed = request.user.listings.filter(is_active=False)
    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    return render(request, "auctions/closed_auctions.html", {
        "user_won": user_won,
        "user_closed": user_closed,
        "listings": Listing.objects.all(),
        "watch_count": watch_count
    })

@login_required
def post_comment(request, article_id):
    if request.method == 'POST':
        content = request.POST["content"]
        c = CommentForm(request.POST)
        if c.is_valid():
            c.save()
            messages.success (request,'Comment posted!')
    url = reverse('listing', kwargs={'article_id': article_id})
    return HttpResponseRedirect(url)

@login_required
def listing(request, article_id):
    current_user = request.user
    l = Listing.objects.get(pk=article_id)
    bid_count = len(l.bid_listing.all())
    try:
        last_bid_amount = l.bid_listing.last().bid_amount
        last_bid_user = l.bid_listing.last().bid_created_by_id
    except:
        last_bid_amount = l.price
        last_bid_user = 'No one'
    
    try:
        watch_count = len(request.user.watchlist.get().products.all())
    except:
        watch_count = 0

    if request.method == 'POST':
        bid_amount = float(request.POST["bid_amount"])
        b = BidForm(request.POST)
        if b.is_valid():
            if bid_amount > l.price and bid_amount > last_bid_amount:
                b.save()
                messages.success (request,'Bid saved successfully')
                bid_count = len(l.bid_listing.all())
                last_bid_amount = bid_amount
                last_bid_user = current_user
            else:
                messages.warning (request, 'Your bid is too low')
    
    c = CommentForm(initial={
            'created_by': request.user,
            'item_commented': Listing.objects.get(pk=article_id)
            })

    b = BidForm(initial={
        'bid_amount': last_bid_amount + 1,
        'bid_listings_id': article_id,
        'bid_created_by_id': current_user
        })

    return render(request, "auctions/listing.html", {
        "l": l,
        "bid_form": b,
        "comment_form": c,
        "bid_count": bid_count,
        "last_bid_amount": last_bid_amount,
        "last_bid_user": last_bid_user,
        "current_user": current_user,
        "watch_count": watch_count
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning (request, 'Invalid Username or Password')
            return render(request, "auctions/login.html")
    else:
        messages.info (request, 'This is a Demo, but you can quick log in with this user!')
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

            new_watchlist = Watchlist.objects.create_watchlist(user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
