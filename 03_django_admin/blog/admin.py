from django.contrib import admin
from blog import models
from django.contrib.admin.models import LogEntry
from django.core import paginator
from django.utils.functional import cached_property


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
