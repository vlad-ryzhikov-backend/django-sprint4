from django.contrib import admin

from .models import Comment, Category, Location, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'created_at',
        'slug',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'location',
        'category',
        'created_at',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title',
        'author__username',
    )
