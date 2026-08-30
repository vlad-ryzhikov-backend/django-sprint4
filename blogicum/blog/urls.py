from django.urls import path

from .views import (
    PostListView,
    PostByCategoryListView,
    PostDetailView, PostCreateView,
    ProfileView, ProfileEditView
    )

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:slug>/',
        PostByCategoryListView.as_view(),
        name='category_posts'
    ),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
]
