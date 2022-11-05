from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['category', 'contents', 'created_at']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'link_tag']

    def link_tag(self, post):
        if post.image_dirs:
            return mark_safe(f'<img src =" {post.image_dirs.url}" height=200px/>')
        return None

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'answer', 'created_at']