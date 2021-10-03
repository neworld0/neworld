from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from neworld.models import WeeklyBible, WBsummary, Bible, PubsIndex
from bs4 import BeautifulSoup
import requests
import datetime
import re
from urllib.parse import urlparse


# 오늘이 몇 주차인지 계산
def get_number_of_week():
    today = datetime.datetime.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    cal = last_monday.isocalendar()
    return cal

cal = get_number_of_week()
target_year = str(cal[0])
target_week = str(cal[1])
target_next_week = str(cal[1]+1)
# target_next_week = str(cal[1])


# 다음주 성서읽기 크롤링 함수
def fetch_weeklybible_latest_data(url, tag):
    result = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    web_page_link_root = 'https://wol.jw.org'
    item = soup.select_one(tag)

    # week
    week = item.find('h1').text
    # bible_range
    bible_range = item.find('h2').text
    # bible_link
    page_link_raw = web_page_link_root + item.find('h2').find('a')['href']
    page_link_parts = urlparse(page_link_raw)
    normalized_page_link = page_link_parts.scheme + '://' + page_link_parts.hostname + page_link_parts.path
    # specific id
    specific_id = page_link_parts.path.split('/')[-3]       # list의 인덱싱 : [-3] -> 끝에서 3번째 요소(/202021321/) 선택
    item_obj = {
        'year': target_year,
        'n_week': target_next_week,
        'week': week,
        'bible_range': bible_range,
        'bible_link': normalized_page_link,
        'create_date': timezone.now(),
        'specific_id': specific_id
    }
    result.append(item_obj)
    return result

# 성서읽기 크롤링 데이터 DB 저장 함수
def add_new_items(crawled_items):
    last_inserted_items = WeeklyBible.objects.last()
    if last_inserted_items is None:
        last_inserted_specific_id = ""
    else:
        last_inserted_specific_id = getattr(last_inserted_items, 'specific_id')

    items_to_insert_into_db = []
    for item in crawled_items:
        if item['specific_id'] == last_inserted_specific_id:
            break
        items_to_insert_into_db.append(item)

    items_to_insert_into_db.reverse()
    for item in items_to_insert_into_db:
        WeeklyBible(
            year=item['year'],
            n_week=item['n_week'],
            week=item['week'],
            bible_range=item['bible_range'],
            bible_link=item['bible_link'],
            create_date=item['create_date'],
            specific_id=item['specific_id']
        ).save()
    return items_to_insert_into_db


# 다음 주의 WBsummary update 준비
def wbsummary_update_prep(target_year, target_next_week):
    weeklybible = WeeklyBible.objects.get(year=target_year, n_week=target_next_week)
    br1 = weeklybible.bible_range
    br2 = br1.strip()
    if '요한 1서' in br2:
        br5 = '요한 1서'
    elif '요한 2서' in br2:
        br5 = '요한 2서'
    elif '요한 3서' in br2:
        br5 = '요한 3서'
    else:
        br3 = re.findall(r'\D+', br2)
        br4 = br3[0]
        br5 = br4.strip()
    br6 = Bible.objects.get(bible=br5)
    br = br6.bible_id
    bible = br6.bible

    bs1 = weeklybible.bible_range
    bs2 = bs1.strip()
    bs3 = re.findall(r'\d+', bs2)
    if len(bs3) > 2:
        bs4 = bs3.pop(0)
    else:
        bs4 = bs3
    b = int(bs4[0])
    c = int(bs4[1])
    bs = c - b
    result = [br, bs, b, c, bible]
    return result

# Outline crawling 파라미터 값 생성
def ws_parameter(ws_update):
    result = []
    url_current = 'https://wol.jw.org/ko/wol/bibledocument/r8/lp-ko/nwtsty/' + ws_update[0] + '/outline'
    for i in range(ws_update[1] + 1):
        tag = '#article > ul > li:nth-child(' + str(ws_update[2] + i) + ')'
        result.append(tag)
    result.append(url_current)
    return result


def fetch_wbsummary_latest_data(url, tag):
    result = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    web_page_link_root = 'https://wol.jw.org'
    for item in tag:
        list_item = soup.select_one(item)
        chapter1 = list_item.find('p').text
        chapter = chapter1.strip()
        bible_summary1 = list_item.find('ul').text
        bible_summary2 = bible_summary1.strip()
        bible_summary3 = bible_summary2.split(')')
        count = len(bible_summary3)
        for i in range(count-1):
            a = bible_summary3[i]
            a1 = re.findall(r'\d+', a)
            if len(a1) < 1:
                a2 = 0
            else:
                a2 = int(a1[len(a1) - 1])
            b = bible_summary3[i + 1]
            b1 = re.findall(r'\d+', b)
            if len(b1) < 1:
                b2 = 0
            else:
                b2 = int(b1[len(b1) - 1])
            if a2 > b2:
                b3 = '- ' + b
                del bible_summary3[i+1]
                bible_summary3.insert(i + 1, b3)
            elif a2 == b2:
                del b
            else:
                del a
        bible_summary3.pop()
        bible_summary4 = []
        for i in range(count-1):
            bible_summary4.append(bible_summary3[i]+')')
        count1 = len(bible_summary4)
        for i in range(count1-1):
            a = bible_summary4[i]
            a1 = re.findall(r'\d+', a)
            a2 = int(a1[len(a1)-1])
            b = bible_summary4[i+1]
            b1 = re.findall(r'\d+', b)
            b2 = int(b1[len(b1)-1])
            if a2 == b2:
                del b
        bible_summary = '\n'.join(bible_summary4)
        page_link_raw = web_page_link_root + list_item.find('p').find('a')['href']
        page_link_parts = urlparse(page_link_raw)
        # specific id
        specific_id = page_link_parts.path.split('/')[-2:]       # list의 인덱싱 : [-2:] -> 끝에서 2번째~마지막 요소(/5/33) 선택
        item_obj = {
            'chapter': chapter,
            'bible_summary': bible_summary,
            'specific_id': specific_id,
            'create_date': timezone.now()
        }
        result.append(item_obj)
    return result


# 크롤링 데이터 DB 저장 함수
def add_wbsummary_new_items(crawled_items, bible_id):
    last_inserted_items = WBsummary.objects.last()
    if last_inserted_items is None:
        last_inserted_specific_id = ""
    else:
        last_inserted_specific_id = getattr(last_inserted_items, 'specific_id')
    items_to_insert_into_db = []
    for item in crawled_items:
        a = last_inserted_specific_id
        b = re.findall(r'\d+', a)
        if item['specific_id'][0] == b[0] and int(item['specific_id'][1]) <= int(b[1]):
            pass
        else:
            items_to_insert_into_db.append(item)

    weeklybible = WeeklyBible.objects.get(year=target_year, n_week=target_next_week)
    bible = get_object_or_404(Bible, pk=bible_id)
    for item in items_to_insert_into_db:
        WBsummary(
            weeklybible=weeklybible,
            bible=bible,
            chapter=item['chapter'],
            bible_summary=item['bible_summary'],
            specific_id=item['specific_id'],
            create_date=item['create_date']
        ).save()
    return items_to_insert_into_db


# 다음 주의 Publications Index update 준비
def pi_update_prep(target_year, target_next_week):
    weeklybible = WeeklyBible.objects.get(year=target_year, n_week=target_next_week)
    br1 = weeklybible.bible_range
    br2 = br1.strip()
    if '요한 1서' in br2:
        br5 = '요한 1서'
    elif '요한 2서' in br2:
        br5 = '요한 2서'
    elif '요한 3서' in br2:
        br5 = '요한 3서'
    else:
        br3 = re.findall(r'\D+', br2)
        br4 = br3[0]
        br5 = br4.strip()
    br6 = Bible.objects.get(bible=br5)
    br = br6.bible_id
    bible = br6.bible

    bs1 = weeklybible.bible_range
    bs2 = bs1.strip()
    bs3 = re.findall(r'\d+', bs2)
    if len(bs3) > 2:
        bs4 = bs3.pop(0)
    else:
        bs4 = bs3
    b = int(bs4[0])
    c = int(bs4[1])
    bs = c - b
    result = [br, bs, b, c, bible]
    return result

# Publications Index crawling 파라미터 값 생성
def pi_parameter(pi_update):
    result = []
    tag = '#studyDiscover > div.section'
    result.append(tag)
    for i in range(pi_update[1] + 1):
        url_current = 'https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/' + str(pi_update[0]) + '/' + str(pi_update[2]+i)
        result.append(url_current)
    return result


def fetch_pilink_latest_data(tag, url1, chapter):
    result = []
    web_page_link_root = 'https://wol.jw.org'
    i = 0
    tag_index = 'div.group.index.collapsible > ul > li.item.ref-dx > span'
    tag_title = 'h3 > span'
    for target in url1:
        response = requests.get(target)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        item_list = soup.select(tag)
        for item in item_list:
            index_verse_find = item.select(tag_index)
            if index_verse_find:
                verse = item.select(tag_title)
                index_verse_str = verse[0]
                index_verse = index_verse_str.text
                for link in index_verse_find:
                    p_list = link.select('p')
                    for p_tag in p_list:
                        if p_tag.text == '':
                            pass
                        else:
                            a_list = p_tag.select('a')
                            for a_tag in a_list:
                                pi_title = a_tag.text
                                href = a_tag['href']
                                pubs_link_raw1 = web_page_link_root + href
                                page_link_parts = urlparse(pubs_link_raw1)
                                normalized_page_link = page_link_parts.scheme + '://' + page_link_parts.hostname + page_link_parts.path
                                specific_id = page_link_parts.path.split('/')[-3:]
                                item_obj = {
                                    'chapter': str(int(chapter) + i),
                                    'index_verse': index_verse,
                                    'pi_title': pi_title,
                                    'pi_link': normalized_page_link,
                                    'specific_id': specific_id,
                                    'create_date': timezone.now()
                                }
                                result.append(item_obj)
        i = i + 1
    result.reverse()
    return result


# 크롤링 데이터 DB 저장 함수
def add_pilink_new_items(crawled_items, bible_id, chapter):
    try:
        last_inserted_items = PubsIndex.objects.last()
    except PubsIndex.DoesNotExist:
        # if last_inserted_items is None:
        last_inserted_specific_id = ""
        PubsIndex.create()
    else:
        last_inserted_specific_id = getattr(last_inserted_items, 'specific_id')
    items_to_insert_into_db = []
    for item in crawled_items:
        if item['specific_id'] == last_inserted_specific_id:
            break
        items_to_insert_into_db.append(item)
    items_to_insert_into_db.reverse()

    weeklybible = WeeklyBible.objects.get(year=target_year, n_week=target_next_week)
    bible = get_object_or_404(Bible, pk=bible_id)
    wbsummary = WBsummary.objects.get(bible=bible_id, chapter=chapter)

    if last_inserted_items.chapter == wbsummary.chapter:
        pass
    else:
        for item in items_to_insert_into_db:
            PubsIndex(
                weeklybible=weeklybible,
                bible=bible,
                chapter=item['chapter'],
                index_verse=item['index_verse'],
                pi_title=item['pi_title'],
                pi_link=item['pi_link'],
                specific_id=item['specific_id'],
                create_date=item['create_date']
            ).save()
    return items_to_insert_into_db


# weeklybible 페이지 호출
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def weeklybible(request):
    # 주간 성서읽기 범위 update 판단
    try:
        weeklybible = WeeklyBible.objects.last()
    except WeeklyBible.DoesNotExist:
        url = 'https://wol.jw.org/ko/wol/meetings/r8/lp-ko/' + target_year + '/' + target_next_week
        tag = '#article > div.todayItems > div.todayItem > div.itemData > header'
        wb = fetch_weeklybible_latest_data(url, tag)
        add_new_items(wb)
        weeklybible = WeeklyBible.objects.last()

    if weeklybible.year == target_year and weeklybible.n_week >= target_next_week:
        pass
    else:
        # 주간 성서읽기 범위 update
        url = 'https://wol.jw.org/ko/wol/meetings/r8/lp-ko/' + target_year + '/' + target_next_week
        tag = '#article > div.todayItems > div.todayItem > div.itemData > header'
        wb = fetch_weeklybible_latest_data(url, tag)
        add_new_items(wb)

    # 페이지 호출
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        weeklybible_list = WeeklyBible.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        weeklybible_list = WeeklyBible.objects.annotate(num_meditation=Count('content')).order_by('-num_content', '-create_date')
    else:  # recent
        weeklybible_list = WeeklyBible.objects.order_by('-n_week')

    # 검색
    if kw:
        weeklybible_list = weeklybible_list.filter(
            Q(year__icontains=kw) |  # 년도 검색
            Q(week__icontains=kw) |  # 성구범위 검색
            Q(content__author__first_name__icontains=kw)  # 성서읽기 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(weeklybible_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'weeklybible_list': page_obj,
               'target_week': target_week,
               'page': page,
               'kw': kw,
               'so': so
               }

    # wbsummary update 여부 판단 및 크롤링
    ws_update = wbsummary_update_prep(target_year, target_next_week)
    pi_update = pi_update_prep(target_year, target_next_week)
    try:
        wbsummary = WBsummary.objects.last()
    except WBsummary.DoesNotExist:
        wp = ws_parameter(ws_update)
        ws = fetch_wbsummary_latest_data(wp[len(wp)-1], wp[0:len(wp)-1])
        add_wbsummary_new_items(ws, ws_update[0])
        wbsummary = WBsummary.objects.last()

    if int(wbsummary.weeklybible.n_week) >= int(target_next_week):
        pass
    else:
        wp = ws_parameter(ws_update)
        ws = fetch_wbsummary_latest_data(wp[len(wp)-1], wp[0:len(wp)-1])
        add_wbsummary_new_items(ws, ws_update[0])
        pi = pi_parameter(pi_update)
        ps = fetch_pilink_latest_data(pi[0], pi[1:], pi_update[2])
        add_pilink_new_items(ps, pi_update[0], pi_update[2])
    return render(request, 'neworld/weeklybible.html', context)


# 주간성서읽기 상세내용 호출
@login_required(login_url='common:login')
# @permission_required('views.permission_view', login_url=reverse_lazy('neworld:goldmembership_guide'))
def weeklybible_detail(request, weeklybible_id):
    weeklybible = get_object_or_404(WeeklyBible, pk=weeklybible_id)
    context = {'weeklybible': weeklybible}
    return render(request, 'neworld/weeklybible_detail.html', context)
