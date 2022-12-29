from django.urls import path

from .views import base_views, scripture_views, meditation_views, question_views, \
    answer_views, comment_views, vote_views, weeklybible_views, research_views, \
    goldmembership_views, customer_views, activity_views, gpt_views, gptanswer_views

app_name = 'neworld'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),

    # goldmembership_views.py
    path('goldmembership_guide/', goldmembership_views.goldmembership_guide, name='goldmembership_guide'),

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
    path('comment/create/customer/<int:customer_id>/',
         comment_views.comment_create_customer, name='comment_create_customer'),
    path('comment/modify/customer/<int:comment_id>/',
         comment_views.comment_modify_customer, name='comment_modify_customer'),
    path('comment/delete/customer/<int:comment_id>/',
         comment_views.comment_delete_customer, name='comment_delete_customer'),
    path('comment/create/activity/<int:activity_id>/',
         comment_views.comment_create_activity, name='comment_create_activity'),
    path('comment/modify/activity/<int:comment_id>/',
         comment_views.comment_modify_activity, name='comment_modify_activity'),
    path('comment/delete/activity/<int:comment_id>/',
         comment_views.comment_delete_activity, name='comment_delete_activity'),
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
    path('comment/create/research/<int:research_id>/',
         comment_views.comment_create_research, name='comment_create_research'),
    path('comment/modify/research/<int:comment_id>/',
         comment_views.comment_modify_research, name='comment_modify_research'),
    path('comment/delete/research/<int:comment_id>/',
         comment_views.comment_delete_research, name='comment_delete_research'),

    path('comment/create/gpt/<int:gpt_id>/',
         comment_views.comment_create_gpt, name='comment_create_gpt'),
    path('comment/modify/gpt/<int:comment_id>/',
         comment_views.comment_modify_gpt, name='comment_modify_gpt'),
    path('comment/delete/gpt/<int:comment_id>/',
         comment_views.comment_delete_gpt, name='comment_delete_gpt'),
    path('comment/create/gptanswer/<int:gptanswer_id>/',
         comment_views.comment_create_gptanswer, name='comment_create_gptanswer'),
    path('comment/modify/gptanswer/<int:comment_id>/',
         comment_views.comment_modify_gptanswer, name='comment_modify_gptanswer'),
    path('comment/delete/gptanswer/<int:comment_id>/',
         comment_views.comment_delete_gptanswer, name='comment_delete_gptanswer'),

    # vote_views.py
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),
    path('vote/scripture/<int:scripture_id>/', vote_views.vote_scripture, name='vote_scripture'),
    path('vote/meditation/<int:meditation_id>/', vote_views.vote_meditation, name='vote_meditation'),
    path('vote/weeklybible/<int:weeklybible_id>/', vote_views.vote_weeklybible, name='vote_weeklybible'),
    path('vote/research/<int:research_id>/', vote_views.vote_research, name='vote_research'),
    path('vote/customer/<int:customer_id>/', vote_views.vote_customer, name='vote_customer'),
    path('vote/activity/<int:activity_id>/', vote_views.vote_activity, name='vote_activity'),
    path('vote/gpt/<int:gpt_id>/', vote_views.vote_gpt, name='vote_gpt'),
    path('vote/gptanswer/<int:gptanswer_id>/', vote_views.vote_gptanswer, name='vote_gptanswer'),

    # weeklybible_views.py
    path('weeklybible/', weeklybible_views.weeklybible, name='weeklybible'),
    path('weeklybible/<int:weeklybible_id>/',
         weeklybible_views.weeklybible_detail, name='weeklybible_detail'),

    # research_views.py
    path('research/create/<int:weeklybible_id>/',
         research_views.research_create, name='research_create'),
    path('research/modify/<int:research_id>/',
         research_views.research_modify, name='research_modify'),
    path('research/delete/<int:research_id>/',
         research_views.research_delete, name='research_delete'),

    # customer_views.py
    path('customer/', customer_views.customer, name='customer'),
    path('customer/<int:customer_id>/',
         customer_views.customer_detail, name='customer_detail'),
    path('customer/create/',
         customer_views.customer_create, name='customer_create'),
    path('customer/modify/<int:customer_id>/',
         customer_views.customer_modify, name='customer_modify'),
    path('customer/delete/<int:customer_id>/',
         customer_views.customer_delete, name='customer_delete'),


    # activity_views.py
    path('activity/create/<int:customer_id>/',
         activity_views.activity_create, name='activity_create'),
    path('activity/modify/<int:activity_id>/',
         activity_views.activity_modify, name='activity_modify'),
    path('activity/delete/<int:activity_id>/',
         activity_views.activity_delete, name='activity_delete'),


    # gpt_views.py
    path('gpt/', gpt_views.gpt, name='gpt'),
    path('gpt/<int:gpt_id>/',
         gpt_views.gpt_detail, name='gpt_detail'),
    path('gpt/create/',
         gpt_views.gpt_create, name='gpt_create'),
    path('gpt/modify/<int:gpt_id>/',
         gpt_views.gpt_modify, name='gpt_modify'),
    path('gpt/delete/<int:gpt_id>/',
         gpt_views.gpt_delete, name='gpt_delete'),

    # gptanswer_views.py
    path('gptanswer/create/<int:gpt_id>/',
         gptanswer_views.gptanswer_create, name='gptanswer_create'),
    path('gptanswer/modify/<int:gptanswer_id>/',
         gptanswer_views.gptanswer_modify, name='gptanswer_modify'),
    path('gptanswer/delete/<int:gptanswer_id>/',
         gptanswer_views.gptanswer_delete, name='gptanswer_delete'),
]