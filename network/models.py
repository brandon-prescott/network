from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Inherits from Django's abstract user class"""
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="post_user")
    content = models.CharField(max_length=280)
    number_of_likes = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}_{str(self.time)}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "number_of_likes": self.number_of_likes,
            "time": self.time
        }

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="like_post")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}_{str(self.time)}"
    

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="follow_user")
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="follow_following")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}_{str(self.following)}"


