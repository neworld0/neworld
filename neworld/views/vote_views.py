from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer, Scripture, Meditation


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


# 묵상 추천 등록
@login_required(login_url='common:login')
def vote_meditation(request, meditation_id):
    meditation = get_object_or_404(Meditation, pk=meditation_id)
    if request.user == meditation.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        meditation.voter.add(request.user)
    return redirect('neworld:daily_scripture', scripture_id=meditation.scripture.id)
