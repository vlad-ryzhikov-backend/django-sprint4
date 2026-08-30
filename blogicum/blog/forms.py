from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy

from .models import Post

User = get_user_model()

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


# редактирование профиля
class UserProfileEditForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')