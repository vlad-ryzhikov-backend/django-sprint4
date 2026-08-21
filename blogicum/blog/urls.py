from django.urls import path

from .views import PostListView, PostByCategoryListView, PostDetailView, PostCreateView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:slug>/',
        PostByCategoryListView.as_view(),
        name='category_posts'
    ),
    path('create/', PostCreateView.as_view(), name='create_post')
]
