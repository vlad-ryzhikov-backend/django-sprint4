from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from blog.models import Category, Post
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.forms import UserCreationForm


from .constants import LIMIT
from .forms import CreatePostForm, UserProfileEditForm

User = get_user_model()

# профиль пользователей
class ProfileView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = LIMIT

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username'],
            is_active=True,
            )
    
    def get_queryset(self):
        return Post.objects.filter(author_id=self.profile.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context
    
# форма регистрации
class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')

class ProfileEditView(UpdateView):
    form_class = UserProfileEditForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')
    
    def get_object(self, queryset = None):
        return self.request.user

# форма сознания нового поста
class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index') 

# все посты
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = LIMIT

    def get_queryset(self):
        return Post.objects.all()
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# посты по категориям
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
    
# выбранный пост
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'    

    def get_queryset(self):
        return Post.objects.all()

