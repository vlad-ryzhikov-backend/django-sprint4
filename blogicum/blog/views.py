from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .constants import LIMIT
from .forms import (CommentForm, PostCreateForm, UserEditForm,
                    UserRegistrationForm)
from .mixins import (CommentEditDeleteMixin, PostEditDeleteMixin,
                     ProfileRedirectMixin)
from .models import Category, Comment, Post

User = get_user_model()


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class CommentDeleteView(CommentEditDeleteMixin, DeleteView):
    model = Comment
    template_name = "blog/comment.html"


class CommentEditView(CommentEditDeleteMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
        )


class PostCreateView(ProfileRedirectMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    PostEditDeleteMixin,
    ProfileRedirectMixin,
    DeleteView
):
    model = Post
    template_name = 'blog/create.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post._base_manager.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].instance = self.get_object()
        return context


class PostEditView(PostEditDeleteMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def get_queryset(self):
        return Post._base_manager.select_related(
            'author', 'category', 'location'
        )

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.object.pk}
        )


class ProfileEditView(ProfileRedirectMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = LIMIT
    context_object_name = 'post'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.user_profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        if self.request.user == self.user_profile:
            queryset = Post._base_manager.filter(
                author=self.user_profile
            ).select_related('author', 'category', 'location')
        else:
            queryset = Post.objects.filter(author=self.user_profile)

        return queryset.annotate(
            comment_count=Count("comments")
        ).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = self.user_profile
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = LIMIT
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostByCategoryListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = LIMIT
    context_object_name = 'post'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug'],
            is_published=True
        )

    def get_queryset(self):
        return self.category.posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(UpdateView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.all()

        return Post._base_manager.filter(
            Q(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            ) | Q(author=self.request.user)
        ).select_related('author', 'location', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related('author')
        return context
