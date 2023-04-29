from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Like, Follow
from .forms import PostForm


def index(request):
    all_posts = Post.objects.all().order_by("-time")
    number_of_posts = len(all_posts)
    return render(request, "network/index.html", {
        "form": PostForm,
        "all_posts": all_posts,
        "number_of_posts": number_of_posts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Save post to database
            new_post = Post(
                user=User.objects.get(id=request.user.id),
                content = form.cleaned_data["content"]
            )
            new_post.save()
            return redirect(index)
    else:
        return redirect(index)
    

def profile(request):
    all_user_posts = Post.objects.filter(user=request.user.id).order_by("-time")
    number_of_posts = len(all_user_posts)

    followers_count = len(Follow.objects.filter(following=request.user.id))
    following_count = len(Follow.objects.filter(user=request.user.id))
    
    return render(request, "network/profile.html", {
        "user": User.objects.get(id=request.user.id),
        "followers_count": followers_count,
        "following_count": following_count,
        "all_user_posts": all_user_posts,
        "number_of_posts": number_of_posts
    })
