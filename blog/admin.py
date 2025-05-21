from django.contrib import admin
from django.utils.safestring import mark_safe


# Register your models here.
from django.contrib import admin
from .models import Category, Post, Comment, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)  # Prevent manual editing
    list_display = ('title', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}"width="150" />')
        return "No image"
    image_preview.short_description = 'Preview'