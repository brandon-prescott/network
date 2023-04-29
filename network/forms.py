from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Form for creating a new post"""
    class Meta:
        model = Post
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
            "placeholder": "What's happening?",
            "class": "form-control"
            })
        }