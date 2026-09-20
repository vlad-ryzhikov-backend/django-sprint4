from django.db import models
from django.db.models import Q
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                pub_date__lte=now,
                category__is_published=True
            )
            .select_related('author', 'category', 'location')
        )

    def smart_filter_for_auth_user(self, user):
        now = timezone.now()
        curent_user = user.username if user.is_authenticated else None

        return (
            super()
            .get_queryset()
            .filter(
                Q(author__username=curent_user)
                | Q(
                    is_published=True,
                    pub_date__lte=now,
                    category__is_published=True
                )
            )
            .select_related('author', 'category', 'location')
        )
