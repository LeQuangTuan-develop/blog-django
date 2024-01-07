from django.contrib import admin
from django.utils.html import format_html_join, format_html

# Register your models here.
from .models import *
from .test import TestModel


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "valid", "name", "domain", "created_at"]
    list_display_links = ('id', 'name')
    list_per_page = 50
    search_fields = ['name']
    ordering = ['-id']
    list_filter = ('domain',)

    # description functions like a model field's verbose_name
    @admin.display(description='valid')
    def valid(self, instance: Blog):

        return format_html('<p class="faq__valid">{}</p>'.format(str(instance.is_valid)))


@admin.register(BlogSeries)
class BlogSeriesAdmin(admin.ModelAdmin):
    list_display = ["id", "is_valid", "name", "domain", "created_at"]
    list_display_links = ('id', 'name')
    list_per_page = 50
    search_fields = ['name']
    ordering = ['-id']
    list_filter = ('domain',)


admin.site.register(TestModel)