from django.shortcuts import render
from neworld.models import Scripture
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
import datetime

logger = logging.getLogger('neworld')

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


# index 페이지 출력 및 일용할 성구 크롤링
def index(request):
    logger.info("INFO 레벨로 출력")

    tmr = datetime.date.today() + datetime.timedelta(1)
    t_day = datetime.date.today()
    seven_day = datetime.date.today() + datetime.timedelta(7)
    Tomorrow = str(tmr.year) + '-' + str(tmr.month).zfill(2) + '-' + str(tmr.day).zfill(2)
    Seventh_day = str(seven_day.year) + '-' + str(seven_day.month).zfill(2) + '-' + str(seven_day.day).zfill(2)
    RealDay = str(t_day.year) + '-' + str(t_day.month).zfill(2) + '-' + str(t_day.day).zfill(2)

    # 크롤링할 일용할 성구 범위 선택
    def date_range(start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        return dates

    def date_range_for_crawling(start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + datetime.timedelta(days=i)).strftime("%Y/%m/%d") for i in range((end - start).days + 1)]
        return dates

    # 무슨 요일인지 계산
    def get_day_of_week(yyyy, mm, dd):
        days = ['월', '화', '수', '목', '금', '토', '일']
        return days[datetime.date(yyyy, mm, dd).weekday()]

    # 1주일 일용할 성구 크롤링
    # y = str(t_day.year)
    # m = str(t_day.month).zfill(2)
    # d = str(t_day.day).zfill(2)
    # target_day = y + '/' + m + '/' + d
    date_range_for_crawling = date_range_for_crawling(Tomorrow, Seventh_day)
    print(date_range_for_crawling)
    date_range = date_range(Tomorrow, Seventh_day)
    last_real_date = Scripture.objects.last()
    if last_real_date.real_date in date_range:
        pass
    else:
        d_week = []
        for i in range(len(date_range_for_crawling)):
            url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + date_range_for_crawling[i]
            r = requests.get(url)
            parser = BeautifulSoup(r.text, 'html.parser')
            scrip1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(3) > p.themeScrp')
            body1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(3) > div.bodyTxt > '
                                      'div.section > div.pGroup > p.sb')
            day_t = datetime.date.today() + datetime.timedelta(i+1)
            yyyy = day_t.year
            mm = day_t.month
            dd = day_t.day
            week_t = get_day_of_week(yyyy, mm, dd)
            d_week.append(week_t)
            print(d_week[i])
            scrip = scrip1.text
            body = body1.text
            scrt = Scripture(scripture=scrip, bodytext=body, real_date=date_range[i], d_week=d_week[i], create_date=timezone.now())
            scrt.save()
            if r.status_code == 200:
                print(r.status_code)
            else:
                pass
    scripture1 = Scripture.objects.get(real_date=RealDay)
    title = scripture1.real_date
    day_of_week = scripture1.d_week
    scripture = scripture1.scripture
    bodyText = scripture1.bodytext
    context = {'today_html': title,
               'day_of_week_html': day_of_week,
               'scripture_html': scripture,
               'bodyText_html': bodyText
            }
    return render(request, 'neworld/index.html', context)