import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect

from .models import User, Post, Like, Follow
from .forms import PostForm
from .utils import get_page_objects, post_content


def index(request):
    all_posts = Post.objects.all().order_by("-time")
    number_of_posts = len(all_posts)

    # Only show 10 posts per page
    page_obj = get_page_objects(request, all_posts)

    return render(request, "network/index.html", {
        "form": PostForm,
        "page_obj": page_obj,
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
    

def profile(request, profile_id):
        all_user_posts = Post.objects.filter(user=profile_id).order_by("-time")
        number_of_posts = len(all_user_posts)

        user = User.objects.get(id=request.user.id)
        profile = User.objects.get(id=profile_id)

        followers = Follow.objects.filter(following=profile_id)
        follower_list = []
        for follower in followers:
            follower_list.append(follower.user)

        if user in follower_list:
            is_following = True
        else:
            is_following = False

        following = Follow.objects.filter(user=profile_id)

        # Only show 10 posts per page
        page_obj = get_page_objects(request, all_user_posts)
        
        return render(request, "network/profile.html", {
            "user": user,
            "profile": profile,
            "is_following": is_following,
            "followers_count": len(followers),
            "following_count": len(following),
            "page_obj": page_obj,
            "number_of_posts": number_of_posts
        })


@login_required(login_url="login")
def follow(request):
    if request.method == "POST":
        profile_id = request.POST["profile_id"]
        follow_action = request.POST["follow_action"]

        if follow_action not in ["follow", "unfollow"]:
            return render(request, "auctions/error.html", {
            "message": "Bad request",
            "code": "400"
            })
        
        if follow_action == "follow":
            new_follow = Follow(
                user = User.objects.get(id=request.user.id),
                following = User.objects.get(id=profile_id)
            )
            new_follow.save()
            return redirect(profile, profile_id=profile_id)
        
        if follow_action == "unfollow":
            user_id = request.user.id
            filter = {"user": user_id, "following": profile_id}
            Follow.objects.filter(**filter).delete()
            return redirect(profile, profile_id=profile_id)

    else:

        user_id = request.user.id
        following = Follow.objects.filter(user=user_id).order_by("-time")

        follow_list = []
        for follow in following:
            follow_list.append(follow.following.id)

        following_posts = Post.objects.filter(user__in=follow_list).order_by("-time")
        number_of_posts = len(following_posts)

        # Only show 10 posts per page
        page_obj = get_page_objects(request, following_posts)
    
        return render(request, "network/following.html", {
            "page_obj": page_obj,
            "number_of_posts": number_of_posts
        })
    

@login_required(login_url="login")
@csrf_protect
def post(request, post_id):
    return post_content(request, post_id) # See utils.py for details


@login_required(login_url="login")
@csrf_protect
def profile_post(request, post_id):
    return post_content(request, post_id) # See utils.py for details