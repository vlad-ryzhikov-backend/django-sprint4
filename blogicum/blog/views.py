from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    DetailView,
    UpdateView
)

from .constants import LIMIT
from .forms import (
    CommentForm,
    PostCreateForm,
    UserRegistrationForm
)
from .mixins import (
    AuthorPermissionMixin,
    CommentBaseMixin,
    PostEditDeleteMixin,
    ProfileRedirectMixin
)
from .models import Category, Comment, Post

User = get_user_model()


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class CommentDeleteView(
    AuthorPermissionMixin,
    CommentBaseMixin,
    DeleteView
):
    pk_url_kwarg = "comment_id"


class CommentEditView(AuthorPermissionMixin, CommentBaseMixin, UpdateView):
    form_class = CommentForm
    pk_url_kwarg = "comment_id"


class CommentCreateView(
    CommentBaseMixin,
    CreateView
):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCreateView(ProfileRedirectMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    AuthorPermissionMixin,
    PostEditDeleteMixin,
    ProfileRedirectMixin,
    DeleteView
):
    model = Post
    template_name = 'blog/create.html'
    context_object_name = 'post'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.smart_filter_for_auth_user(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].instance = self.get_object()
        return context


class PostEditView(AuthorPermissionMixin, PostEditDeleteMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def get_queryset(self):
        return Post.objects.smart_filter_for_auth_user(self.request.user)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class ProfileEditView(ProfileRedirectMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
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
        return (
            Post.objects.smart_filter_for_auth_user(self.request.user)
            .filter(author=self.user_profile)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

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
        return (
            Post.objects.filter(category=self.category)
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.smart_filter_for_auth_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context
