import json
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Post, Like, User


def get_page_objects(request, posts):
    """Accepts GET request and a list of posts as arguments and splits up groups of 10 posts per page"""
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


def post_content(request, post_id):
    """Function updates the content of a post if POST request, and returns a JSON of the post content if GET request"""
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Update post contents if input is valid
    elif request.method == "POST":
        data = json.loads(request.body)
        if data.get("content") is not None:
            if data["content"] == "" or data["content"].isspace() == True:
                return HttpResponse(status=400)
            else:
                post.content = data["content"]
                post.save()
                return HttpResponse(status=204)
    
    # Post must be via GET or POST
    else:
        return JsonResponse({"error": "GET or POST request required."}, status=400)
    

def update_likes(request, post_id):
    """Function will like or unlike a post based on if the user has already liked the post or not"""
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Update likes if input is valid
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("action") is not None:
            if data["action"] not in ["like", "unlike"]:
                return HttpResponse(status=400)
            elif data["action"] == "like":
                user_id = request.user.id
                filter = {"user": user_id, "post": post_id}
                if len(Like.objects.filter(**filter)) == 0:
                    number_of_likes = post.number_of_likes
                    number_of_likes += 1
                    post.number_of_likes = number_of_likes
                    post.save()

                    new_like = Like(
                        user = User.objects.get(id=request.user.id),
                        post = Post.objects.get(id=post_id)
                    )
                    new_like.save()
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=400)
            else:
                user_id = request.user.id
                filter = {"user": user_id, "post": post_id}
                if len(Like.objects.filter(**filter)) == 1:
                    number_of_likes = post.number_of_likes
                    number_of_likes -= 1
                    post.number_of_likes = number_of_likes
                    post.save()

                    user_id = request.user.id
                    filter = {"user": user_id, "post": post_id}
                    Like.objects.filter(**filter).delete()

                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=400)

    # Post must be via POST
    else:
        return JsonResponse({"error": "POST request required."}, status=400)