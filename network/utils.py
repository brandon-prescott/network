from django.core.paginator import Paginator


def get_page_objects(request, posts):
    """Accepts GET request and a list of posts as arguments and splits up groups of 10 posts per page"""
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj