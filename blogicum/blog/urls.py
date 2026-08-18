from django.urls import path

from . import views
from .views import PostListView, PostByCategoryListView, PostDetailView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostByCategoryListView.as_view(), name='category_posts'),
]
