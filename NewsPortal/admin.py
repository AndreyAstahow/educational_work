from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Author, Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'post_class', 'author', 'rating')
    list_filter = ('headline', 'post_class', 'author', 'rating')
    search_fields = ('headline', 'post_class__name', 'author', 'rating')

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdminTranslate(TranslationAdmin):
    model = Post

# Register your models here.

admin.site.register(Author)
# admin.site.register(Post, PostAdmin)

admin.site.register(Category)
admin.site.register(Post)