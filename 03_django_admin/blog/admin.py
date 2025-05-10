from django.contrib import admin
from blog import models


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'created_at']
    date_hierarchy = 'created_at'


admin.site.register(models.Blog, BlogAdmin)
