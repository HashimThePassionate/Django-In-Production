from django.contrib import admin
from blog import models


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'created_at', 'letter_count']
    date_hierarchy = 'created_at'

    def letter_count(self, obj):
        return sum(1 for c in obj.content if c.isalpha())


admin.site.register(models.Blog, BlogAdmin)
