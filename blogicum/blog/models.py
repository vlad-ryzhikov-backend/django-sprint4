from core.models import BaseModel
from django.auth import get_user_model
from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars

from .constants import MAX_LENGTH, TITLE_DISPLAY_LENGTH
from .managers import PublishedManager

User = get_user_model()


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
    image = models.ImageField(
        "Изображение",
        upload_to="blogicum_images",
        blank=True
    )

    objects = PublishedManager()

    class Meta(BaseModel.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-pub_date']

    def __str__(self):
        return truncatechars(self.title, TITLE_DISPLAY_LENGTH)


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']

    def __str__(self):
        return f"Комментарий от {self.author.username}"
