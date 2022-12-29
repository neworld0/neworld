from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import Gpt, GptAnswer
from ..forms import GptAnswerForm


# Bulletin Board 답변등록
@login_required(login_url='common:login')
def gptanswer_create(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    if request.method == "POST":
        form = GptAnswerForm(request.POST)
        if form.is_valid():
            gptanswer = form.save(commit=False)
            gptanswer.author = request.user
            gptanswer.create_date = timezone.now()
            gptanswer.gpt = gpt
            gptanswer.save()
            return redirect('{}#gptanswer_{}'.format(
                resolve_url('neworld:gpt_detail', gpt_id=gpt.id), gptanswer.id))
    else:
        form = GptAnswerForm()
    context = {'gpt': gpt, 'form': form}
    return render(request, 'neworld/gpt_detail.html', context)


# Bulletin Board 답변 수정
@login_required(login_url='common:login')
def gptanswer_modify(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.user != gptanswer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)
    if request.method == "POST":
        form = GptAnswerForm(request.POST, instance=gptanswer)
        if form.is_valid():
            gptanswer = form.save(commit=False)
            gptanswer.modify_date = timezone.now()
            gptanswer.save()
            return redirect('{}#gptanswer_{}'.format(
                resolve_url('neworld:detail', gpt_id=gptanswer.gpt.id), gptanswer.id))
    else:
        form = GptAnswerForm(instance=gptanswer)
    context = {'gptanswer': gptanswer, 'form': form}
    return render(request, 'neworld/gptanswer_form.html', context)


# Bulletin Board 답변 삭제
@login_required(login_url='common:login')
def gptanswer_delete(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.user != gptanswer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        gptanswer.delete()
    return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)

