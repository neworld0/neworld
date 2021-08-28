from django.shortcuts import render
import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
import os
import django
from neworld.models import Scripture

logger = logging.getLogger('neworld')


# index 페이지 생성
def index(request):

    logger.info("INFO 레벨로 출력")

    tmr = datetime.date.today() + datetime.timedelta(1)
    t_day = datetime.date.today()
    Tomorrow = str(tmr.year) + '-' + str(tmr.month).zfill(2) + '-' + str(tmr.day).zfill(2)
    RealDay = str(t_day.year) + '-' + str(t_day.month).zfill(2) + '-' + str(t_day.day).zfill(2)

    def date_range(start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        return dates

    # 요일 표시
    def get_day_of_week(yyyy, mm, dd):
        days = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
        return days[datetime.date(yyyy, mm, dd).weekday()]

    yyyy = tmr.year
    mm = tmr.month
    dd = tmr.day

    d_week = get_day_of_week(yyyy, mm, dd)

    dates = date_range(Tomorrow, Tomorrow)
    # for i in dates:
    url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + dates[0]
    r = requests.get(url)
    parser = BeautifulSoup(r.text, 'html.parser')
    s = parser.find_all('p', {'class': 'themeScrp'})
    scrip = s[0].text
    bt = parser.find_all('p', {'class': 'sb'})
    body = bt[0].text
    Scripture(scripture=scrip, bodytext=body, real_date=dates[0], d_week=d_week, create_date=timezone.now()).save()

    title = RealDay

    # def scripture():
    #     t = datetime.today() + timedelta(1)
    #     y = str(t.year)
    #     m = str(t.month).zfill(2)
    #     d = str(t.day).zfill(2)
    #     today = y + '/' + m + '/' + d
    #     url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + today
    #     r = requests.get(url)
    #     parser = BeautifulSoup(r.text, 'html.parser')
    #     s = parser.find_all('p', {'class': 'themeScrp'})
    #     scrip = s[0].text
    #     return scrip
    #
    # def bodyText():
    #     t = datetime.today() + timedelta(1)
    #     y = str(t.year)
    #     m = str(t.month).zfill(2)
    #     d = str(t.day).zfill(2)
    #     today = y + '/' + m + '/' + d
    #     url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + today
    #     r = requests.get(url)
    #     parser = BeautifulSoup(r.text, 'html.parser')
    #     bt = parser.find_all('div', {'class': 'bodyTxt'})
    #     body = bt[0].text
    #     return body

    s = Scripture.objects.get(real_date=RealDay)
    # if s.real_date == RealDay:
    scripture = s.scripture
    bodyText = s.bodytext
    # else:
    #     script_ = scripture()
    #     body_ = bodyText()
        # s1 = Scripture(scripture=script_, bodytext=body_, real_date=RealDay, create_date=timezone.now())
        # s1.save()
        # scripture = s1.scripture
        # bodyText = s1.bodytext
        # obj, created = Scripture.objects.get(real_date=RealDay).get_or_create(
        #     scripture=script_,
        #     bodytext=body_,
        #     real_date=RealDay,
        #     create_date=timezone.now()
        # )
        # scripture = obj.scripture
        # bodyText = obj.bodytext

    pageId = ''
    # RealDay = ''
    # scripture = ''
    # bodyText = ''
    # title = ''
    meditation = ''
    # getDir = getDir()
    create_action = ''
    update_action = ''
    delete_dir = ''

    context = {'today_html': RealDay,
               'scripture_html': scripture,
               'bodyText_html': bodyText,
               'title_html': title,
               'meditation_html': meditation,
               # 'listStr_html': getDir,
               'create_action': create_action,
               'update_action': update_action,
               'delete_action': delete_dir
    }
    return render(request, 'neworld/index.html', context)

