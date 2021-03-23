from django.contrib import admin
from .models import Article
from markdownx.admin import MarkdownxModelAdmin


#admin.site.register(Article, MarkdownxModelAdmin) 

@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag_list')
    list_display_links = ('id', 'title')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())