from django.contrib import admin
from blog import models
from django.contrib.admin.models import LogEntry
from django.core import paginator
from django.utils.functional import cached_property
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999


class BlogAdmin(admin.ModelAdmin):
    actions = ('print_blog_titles',)
    paginator = CustomPaginator
    list_per_page = 3
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'created_at', 'letter_count', 'author_full_name']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    filter_vertical = ['tags']
    raw_id_fields = ['author']

    @admin.action(description='Print blog titles')
    def print_blog_titles(self, request, queryset):
        # Saare titles ek list mein collect karo
        titles = [blog.title for blog in queryset]
        # Titles ko string mein convert karo
        message = "Selected Blog Titles: " + ", ".join(titles)
        # Admin panel mein message dikhao
        self.message_user(request, message, level=messages.SUCCESS)

    def author_full_name(self, obj):
        return f'{obj.author.user.first_name} {obj.author.user.last_name}'

    def letter_count(self, obj):
        return sum(1 for c in obj.content if c.isalpha())

    def get_queryset(self, request):
        default_queryset = super().get_queryset(request)
        improved_queryset = default_queryset.select_related(
            'author', 'author__user')
        return improved_queryset


admin.site.register(models.Blog, BlogAdmin)
