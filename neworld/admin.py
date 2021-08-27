from django.contrib import admin
from .models import Question, Scripture, Answer, Meditation, Comment

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)

class ScriptureAdmin(admin.ModelAdmin):
    search_fields = ['real_date']

admin.site.register(Scripture, ScriptureAdmin)

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Answer, AnswerAdmin)


class MeditationAdmin(admin.ModelAdmin):
    search_fields = ['real_date']

admin.site.register(Meditation, MeditationAdmin)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)
