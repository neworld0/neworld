from django.urls import path

from .views import base_views, scripture_views, meditation_views, question_views, answer_views, comment_views, vote_views

app_name = 'neworld'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),

    # scripture_views.py
    path('scripture/',
         scripture_views.scripture, name='scripture'),
    path('scripture/<int:scripture_id>/',
         scripture_views.daily_scripture, name='daily_scripture'),

    # meditation_views.py
    path('meditation/create/<int:scripture_id>/',
         meditation_views.meditation_create, name='meditation_create'),
    path('meditation/modify/<int:meditation_id>/',
         meditation_views.meditation_modify, name='meditation_modify'),
    path('meditation/delete/<int:meditation_id>/',
         meditation_views.meditation_delete, name='meditation_delete'),

    # question_views.py
    path('question/', question_views.question, name='question'),
    path('question/<int:question_id>/',
         question_views.detail, name='detail'),
    path('question/create/',
         question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/',
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',
         answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/',
         comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/',
         comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/',
         comment_views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/',
         comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/',
         comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/',
         comment_views.comment_delete_answer, name='comment_delete_answer'),
    path('comment/create/meditation/<int:meditation_id>/',
         comment_views.comment_create_meditation, name='comment_create_meditation'),
    path('comment/modify/meditation/<int:comment_id>/',
         comment_views.comment_modify_meditation, name='comment_modify_meditation'),
    path('comment/delete/meditation/<int:comment_id>/',
         comment_views.comment_delete_meditation, name='comment_delete_meditation'),

    # vote_views.py
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),
    path('vote/scripture/<int:scripture_id>/', vote_views.vote_scripture, name='vote_scripture'),
    path('vote/meditation/<int:meditation_id>/', vote_views.vote_meditation, name='vote_meditation'),
]
