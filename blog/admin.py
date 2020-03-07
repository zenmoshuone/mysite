from django.contrib import admin
from .models import Blog, BlogType


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'blog_type', 'created_time', 'update_time')


@admin.register(BlogType)
class BlogType(admin.ModelAdmin):
    list_display = ('id', 'type_name')
