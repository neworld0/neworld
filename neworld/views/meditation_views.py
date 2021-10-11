from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from ..forms import MeditationForm
from ..models import Scripture, Meditation
import datetime


# 묵상내용 등록
@login_required(login_url='common:login')
# @permission_required('views.permission_create', login_url=reverse_lazy('neworld:goldmembership_guide'))
def meditation_create(request, scripture_id):
    scripture = get_object_or_404(Scripture, pk=scripture_id)
    user = get_object_or_404(User, pk=request.user.id)
    groups = user.groups.all()
    if request.method == "POST":
        form = MeditationForm(request.POST)
        if form.is_valid():
            meditation = form.save(commit=False)
            meditation.author = request.user  # author 속성에 로그인 계정 저장
            meditation.create_date = timezone.now()
            meditation.real_date = scripture
            meditation.scripture = scripture
            for group in groups:
                meditation.group = group
            meditation.save()
            return redirect('{}#meditation_{}'.format(
                resolve_url('neworld:daily_scripture', scripture_id=scripture.id), meditation.id))
    else:
        form = MeditationForm()
    context = {'scripture': scripture, 'form': form}
    return render(request, 'neworld/daily_scripture.html', context)


# Meditation 내용 수정
@login_required(login_url='common:login')
# @permission_required('views.permission_modify', login_url=reverse_lazy('neworld:goldmebership_guide'))
def meditation_modify(request, meditation_id):
    meditation = get_object_or_404(Meditation, pk=meditation_id)
    if request.user != meditation.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:daily_scripture', scripture_id=meditation.scripture.id)
    if request.method == "POST":
        form = MeditationForm(request.POST, instance=meditation)
        if form.is_valid():
            meditation = form.save(commit=False)
            meditation.modify_date = timezone.now()
            meditation.save()
            return redirect('{}#meditation_{}'.format(
                resolve_url('neworld:daily_scripture', scripture_id=meditation.scripture.id), meditation.id))
    else:
        form = MeditationForm(instance=meditation)
    context = {'meditation': meditation, 'form': form}
    return render(request, 'neworld/meditation_form.html', context)


# Meditation 삭제
@login_required(login_url='common:login')
# @permission_required('views.permission_delete', login_url=reverse_lazy('neworld:goldmebership_guide'))
def meditation_delete(request, meditation_id):
    meditation = get_object_or_404(Meditation, pk=meditation_id)
    if request.user != meditation.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        meditation.delete()
    return redirect('neworld:daily_scripture', scripture_id=meditation.scripture.id)
