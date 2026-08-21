from core.models import BaseModel
from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars

from .constants import MAX_LENGTH, TITLE_DISPLAY_LENGTH
from .managers import PublishedManager


class Category(BaseModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        allow_unicode=True,
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta(BaseModel.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return truncatechars(self.title, TITLE_DISPLAY_LENGTH)


class Location(BaseModel):
    name = models.CharField("Название места", max_length=MAX_LENGTH)

    class Meta(BaseModel.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=False,
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )

    objects = PublishedManager()

    class Meta(BaseModel.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-pub_date']

    def __str__(self):
        return truncatechars(self.title, TITLE_DISPLAY_LENGTH)
