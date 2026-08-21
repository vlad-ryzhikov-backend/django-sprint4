from django import forms

from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'text',
            'pub_date', 'location',
            'category'
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            )
        }