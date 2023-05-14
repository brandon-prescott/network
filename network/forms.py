from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Form for creating a new post"""
    class Meta:
        model = Post
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
            "id": "create-textarea",    
            "placeholder": "What's happening?",
            "class": "form-control",
            "rows": 6
            })
        }
