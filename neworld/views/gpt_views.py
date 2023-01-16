from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from ..models import Gpt
from ..forms import GptForm


# 게시판 목록 출력
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def gpt(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    # 정렬
    if so == 'recommend':
        gpt_list = Gpt.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        gpt_list = Gpt.objects.annotate(num_answer=Count('gptanswer')).order_by('-num_answer', '-create_date')
    else:  # recent
        gpt_list = Gpt.objects.order_by('-create_date')
    # 검색
    if kw:
        gpt_list = gpt_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__first_name__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__first_name__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(gpt_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'gpt_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'neworld/gpt_list.html', context)


# Bulletin Board 상세내용 출력
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def gpt_detail(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    user = User.objects.get(username=request.user)
    groups = user.groups.all()
    group = []
    for g in groups:
        gr = g.id
        group.append(gr)
    context = {'gpt': gpt, 'group_list': group}
    return render(request, 'neworld/gpt_detail.html', context)




# Bulletin Board 질문등록
@login_required(login_url='common:login')
# @permission_required('views.permission_create', login_url=reverse_lazy('neworld:goldmembership_guide'))
def gpt_create(request):
    user = get_object_or_404(User, pk=request.user.id)
    groups = user.groups.all()
    if request.method == 'POST':
        form = GptForm(request.POST)
        if form.is_valid():
            gpt = form.save(commit=False)
            gpt.author = request.user  # author 속성에 로그인 계정 저장
            gpt.create_date = timezone.now()
            for group in groups:
                gpt.group = group
            gpt.save()
            return redirect('neworld:gpt')
    else:
        form = GptForm()
    context = {'form': form}
    return render(request, 'neworld/gpt_form.html', context)


# Bulletin Board 질문 수정
@login_required(login_url='common:login')
# @permission_required('views.permission_change', login_url=reverse_lazy('blog:goldmembership_guide'))
def gpt_modify(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    if request.user != gpt.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=gpt.id)
    if request.method == "POST":
        form = GptForm(request.POST, instance=gpt)
        if form.is_valid():
            gpt = form.save(commit=False)
            gpt.modify_date = timezone.now()  # 수정일시 저장
            gpt.save()
            return redirect('neworld:gpt_detail', gpt_id=gpt.id)
    else:
        form = GptForm(instance=gpt)
    context = {'form': form}
    return render(request, 'neworld/gpt_form.html', context)


# Bulletin Board 질문 삭제
@login_required(login_url='common:login')
# @permission_required('views.permission_delete', login_url=reverse_lazy('neworld:goldmembership_guide'))
def gpt_delete(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    if request.user != gpt.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=gpt.id)
    gpt.delete()
    return redirect('neworld:gpt')