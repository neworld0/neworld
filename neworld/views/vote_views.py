from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer, Scripture, Meditation, WeeklyBible, Research, Customer, Activity, Gpt, GptAnswer


# 질문 추천 등록
@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('neworld:detail', question_id=question.id)


# 답글 추천 등록
@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('neworld:detail', question_id=answer.question.id)


# Scripture 추천 등록
@login_required(login_url='common:login')
def vote_scripture(request, scripture_id):
    scripture = get_object_or_404(Scripture, pk=scripture_id)
    if request.user == scripture.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        scripture.voter.add(request.user)
    return redirect('neworld:daily_scripture', scripture_id=scripture.id)


# Meditation 추천 등록
@login_required(login_url='common:login')
def vote_meditation(request, meditation_id):
    meditation = get_object_or_404(Meditation, pk=meditation_id)
    if request.user == meditation.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        meditation.voter.add(request.user)
    return redirect('neworld:daily_scripture', scripture_id=meditation.scripture.id)



# Weeklybible 추천 등록
@login_required(login_url='common:login')
def vote_weeklybible(request, weeklybible_id):
    weeklybible = get_object_or_404(WeeklyBible, pk=weeklybible_id)
    if request.user == weeklybible.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        weeklybible.voter.add(request.user)
    return redirect('neworld:weeklybible_detail', weeklybible_id=weeklybible.id)


# Research 추천 등록
@login_required(login_url='common:login')
def vote_research(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    if request.user == research.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        research.voter.add(request.user)
    return redirect('neworld:weeklybible_detail', weeklybible_id=research.weeklybible.id)


# 고객 추천 등록
@login_required(login_url='common:login')
def vote_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.user == customer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        customer.voter.add(request.user)
    return redirect('neworld:customer_detail', customer_id=customer.id)


# 활동 추천 등록
@login_required(login_url='common:login')
def vote_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.user == activity.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        activity.voter.add(request.user)
    return redirect('neworld:customer_detail', customer_id=activity.customer.id)


# Gpt 추천 등록
@login_required(login_url='common:login')
def vote_gpt(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    if request.user == gpt.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        gpt.voter.add(request.user)
    return redirect('neworld:gpt_detail', gpt_id=gpt.id)


# GptAnswer 추천 등록
@login_required(login_url='common:login')
def vote_gptanswer(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.user == gptanswer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        gptanswer.voter.add(request.user)
    return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)