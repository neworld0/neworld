from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from ..forms import CustomerForm
from ..models import Customer


# 게시판 목록 출력
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def customer(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    # 정렬
    if so == 'recommend':
        customer_list = Customer.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        customer_list = Customer.objects.annotate(num_activity=Count('activity')).order_by('-num_activity', '-create_date')
    else:  # recent
        customer_list = Customer.objects.order_by('-create_date')
    # 검색
    if kw:
        customer_list = customer_list.filter(
            Q(area__icontains=kw) |  # 지역 검색
            Q(name__icontains=kw) |  # 단체명 검색
            Q(keyman__icontains=kw) |  # 키맨 검색
            Q(position__icontains=kw) |  # 직위 검색
            Q(grade__icontains=kw)  #  추진등급 검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(customer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'customer_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'neworld/customer_list.html', context)


# Bulletin Board 상세내용 출력
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def customer_detail(request, customer_id):
    customer_c = get_object_or_404(Customer, pk=customer_id)
    user = User.objects.get(username=request.user)
    groups = user.groups.all()
    group = []
    for g in groups:
        gr = g.id
        group.append(gr)
    context = {'customer': customer_c, 'group_list': group}
    return render(request, 'neworld/customer_detail.html', context)


# Customer 정보 등록
@login_required(login_url='common:login')
# @permission_required('views.permission_create', login_url=reverse_lazy('neworld:goldmembership_guide'))
def customer_create(request):
    user = get_object_or_404(User, pk=request.user.id)
    groups = user.groups.all()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.author = request.user  # author 속성에 로그인 계정 저장
            customer.create_date = timezone.now()
            for group in groups:
                customer.group = group
            customer.save()
            return redirect('neworld:customer')
    else:
        form = CustomerForm()
    context = {'form': form}
    return render(request, 'neworld/customer_form.html', context)


# Customer 정보 수정
@login_required(login_url='common:login')
# @permission_required('views.permission_change', login_url=reverse_lazy('blog:goldmembership_guide'))
def customer_modify(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.user != customer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=customer.id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.modify_date = timezone.now()  # 수정일시 저장
            customer.save()
            return redirect('neworld:customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    context = {'form': form}
    return render(request, 'neworld/customer_form.html', context)


# Customer 정보 삭제
@login_required(login_url='common:login')
# @permission_required('views.permission_delete', login_url=reverse_lazy('neworld:goldmembership_guide'))
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.user != customer.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=customer.id)
    customer.delete()
    return redirect('neworld:customer')
