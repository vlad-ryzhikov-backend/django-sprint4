from django.db import models
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
                category__is_published=True,
            )
        )
