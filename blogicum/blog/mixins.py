from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment

# Столкнулся с проблемой: происходит редирект на страницу поста,
# но во всех CBV, где использую данный миксин, получаю лишние
# запросы к БД. Искал решение, так и не понял. Есть вариант
# работы с кэшем, но в проекте отказался от реализации, так как
# думаю, что есть варианты легче. Буду благодарен за подсказку)).

class AuthorPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostEditDeleteMixin:
    pk_url_kwarg = 'post_id'


class CommentBaseMixin(LoginRequiredMixin):
    model = Comment
    template_name = "blog/comment.html"

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class ProfileRedirectMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
