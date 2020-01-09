from django.contrib import admin

from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BlogPost._meta.fields]

    class Meta:
        model = BlogPost

admin.site.register(BlogPost, BlogPostAdmin)