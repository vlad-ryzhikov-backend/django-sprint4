from django.forms import DateTimeInput
from django.urls import reverse_lazy
from blog.models import Category, Post
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView

from .constants import LIMIT
from .forms import CreatePostForm

class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index') 

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = LIMIT

    def get_queryset(self):
        return Post.objects.all()


class PostByCategoryListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = LIMIT
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug'],
            is_published=True,
        )
    
    def get_queryset(self):
        return Post.objects.filter(category_id=self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


    def get_queryset(self):
        return Post.objects.all()

