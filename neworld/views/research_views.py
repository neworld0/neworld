from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.models import User
from ..forms import ResearchForm
from ..models import WeeklyBible, Research


# 조사내용 등록
@login_required(login_url='common:login')
def research_create(request, weeklybible_id):
    weeklybible = get_object_or_404(WeeklyBible, pk=weeklybible_id)
    user = get_object_or_404(User, pk=request.user.id)
    groups = user.groups.all()
    if request.method == "POST":
        form = ResearchForm(request.POST)
        if form.is_valid():
            research = form.save(commit=False)
            research.author = request.user  # author 속성에 로그인 계정 저장
            research.create_date = timezone.now()
            research.weeklybible = weeklybible
            for group in groups:
                research.group = group
            research.save()
            return redirect('{}#research_{}'.format(
                resolve_url('neworld:weeklybible_detail', weeklybible_id=weeklybible.id), research.id))
    else:
        form = ResearchForm()
    context = {'weeklybible': weeklybible, 'form': form}
    return render(request, 'neworld/weeklybible_detail.html', context)


# Research content 내용 수정
@login_required(login_url='common:login')
def research_modify(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    if request.user != research.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:weeklybible_detail', weeklybible_id=research.weeklybible.id)
    if request.method == "POST":
        form = ResearchForm(request.POST, instance=research)
        if form.is_valid():
            research = form.save(commit=False)
            research.modify_date = timezone.now()
            research.save()
            return redirect('{}#research_{}'.format(
                resolve_url('neworld:weeklybible_detail', weeklybible_id=research.weeklybible.id), research.id))
    else:
        form = ResearchForm(instance=research)
    context = {'research': research, 'form': form}
    return render(request, 'neworld/research_form.html', context)


# Research content 삭제
@login_required(login_url='common:login')
def research_delete(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    if request.user != research.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        research.delete()
    return redirect('neworld:weeklybible_detail', weeklybible_id=research.weeklybible.id)
