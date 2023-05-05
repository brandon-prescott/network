import json
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Post


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