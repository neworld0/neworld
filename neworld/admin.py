from django.contrib import admin
from neworld.models import Question, Scripture, Answer, Meditation, Comment, WeeklyBible, Research, Bible, WBsummary, PubsIndex


# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['username']
#
# admin.site.register(User, UserAdmin)


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


class WeeklyBibleAdmin(admin.ModelAdmin):
    search_fields = ['n_week']

admin.site.register(WeeklyBible, WeeklyBibleAdmin)


class ResearchAdmin(admin.ModelAdmin):
    search_fields = ['n_week']

admin.site.register(Research, ResearchAdmin)


class BibleAdmin(admin.ModelAdmin):
    search_fields = ['bible']

admin.site.register(Bible, BibleAdmin)


class WBsummaryAdmin(admin.ModelAdmin):
    search_fields = ['bible_summary']

admin.site.register(WBsummary, WBsummaryAdmin)


class PubsIndexAdmin(admin.ModelAdmin):
    search_fields = ['pi_title']

admin.site.register(PubsIndex, PubsIndexAdmin)
