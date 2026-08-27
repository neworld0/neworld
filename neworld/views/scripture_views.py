from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
from ..models import Scripture, Meditation
from django.contrib.auth.models import User
from common.decorators import allowed_users, son123_only


# 성구 목록 출력
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def scripture(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    d_today = str(datetime.date.today())

    # 정렬
    if so == 'recommend':
        scripture_list = Scripture.objects.annotate(num_voter=Count('meditation__voter'))
    elif so == 'popular':
        scripture_list = Scripture.objects.annotate(num_meditation=Count('meditation'))
    else:  # recent
        scripture_list = Scripture.objects.all()

    # 검색
    if kw:
        scripture_list = scripture_list.filter(
            Q(scripture__icontains=kw) |  # 성구검색
            Q(bodytext__icontains=kw) |  # 해설검색
            Q(meditation__author__first_name__icontains=kw)  # 묵상 글쓴이검색
        ).distinct()
    scripture_list = scripture_list.annotate(
        today_rank=Case(When(real_date=d_today, then=Value(0)), default=Value(1), output_field=IntegerField())
    )
    if so == 'recommend':
        scripture_list = scripture_list.order_by('today_rank', '-num_voter', '-create_date')
    elif so == 'popular':
        scripture_list = scripture_list.order_by('today_rank', '-num_meditation', '-create_date')
    else:
        scripture_list = scripture_list.order_by('today_rank', '-create_date')


    # 페이징처리
    paginator = Paginator(scripture_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    today_scripture = (Scripture.objects.filter(real_date=d_today).exclude(scripture="").exclude(bodytext="")
                        .order_by("id").first())
    context = {'scripture_list': page_obj, 'today_scripture': today_scripture,
               'd_today': d_today, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'neworld/scripture_list.html', context)


# 성구 상세내용 출력
@login_required(login_url='common:login')
# @allowed_users(allowed_roles=['321son'])
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def daily_scripture(request, scripture_id):
    scripture = get_object_or_404(Scripture, pk=scripture_id)
    user = User.objects.get(username=request.user)
    groups = user.groups.all()
    group = []
    for g in groups:
        gr = g.id
        group.append(gr)
    context = {'scripture': scripture, 'group_list': group}
    return render(request, 'neworld/daily_scripture.html', context)
