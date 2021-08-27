from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer



# Bulletin Board 답변등록
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('neworld:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'neworld/question_detail.html', context)


# Bulletin Board 답변 수정
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer_m= get_object_or_404(Answer, pk=answer_id)
    if request.user != answer_m.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:detail', question_id=answer_m.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer_m)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('neworld:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer_m)
    context = {'answer_m': answer_m, 'form': form}
    return render(request, 'neworld/answer_form.html', context)


# Bulletin Board 답변 삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer_dl = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer_dl.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer_dl.delete()
    return redirect('neworld:detail', question_id=answer_dl.question.id)

