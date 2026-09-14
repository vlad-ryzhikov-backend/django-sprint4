from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post

User = get_user_model()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Оставьте комментарий'
                }
            )
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email'
        )
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
        
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        )
        
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }