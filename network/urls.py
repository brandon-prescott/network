
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/post/<int:post_id>", views.profile_post, name="profile_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/like/<int:post_id>", views.profile_like, name="profile_like"),
    path("follow/post/<int:post_id>", views.following_like, name="following_like")
]
