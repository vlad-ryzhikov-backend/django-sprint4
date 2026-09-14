from django.urls import path

from .views import (CommentCreateView, CommentDeleteView, CommentEditView,
                    PostByCategoryListView, PostCreateView, PostDeleteView,
                    PostDetailView, PostEditView, PostListView,
                    ProfileEditView, ProfileView)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path(
        'category/<slug:slug>/',
        PostByCategoryListView.as_view(),
        name='category_posts'
    ),

    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'posts/<int:post_id>/edit/',
        PostEditView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),

    path(
        "posts/<int:post_id>/comment/",
        CommentCreateView.as_view(),
        name="add_comment"
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        CommentEditView.as_view(),
        name="edit_comment"
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        CommentDeleteView.as_view(),
        name="delete_comment"
    ),

    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]
