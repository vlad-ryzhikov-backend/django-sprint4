from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Comment


class PostEditDeleteMixin:
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        if not hasattr(self, '_cached_object'):
            if queryset is None:
                queryset = self.get_queryset()

            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])

        obj = self.get_object()

        if obj.author != request.user:
            return redirect('blog:post_detail', pk=obj.pk)

        return super().dispatch(request, *args, **kwargs)


class CommentEditDeleteMixin(LoginRequiredMixin):
    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs['comment_id'])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_authenticated or obj.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
        )


class ProfileRedirectMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
