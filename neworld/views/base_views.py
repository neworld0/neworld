from django.shortcuts import render
from neworld.models import Scripture
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
import datetime

logger = logging.getLogger('neworld')

# index 페이지 출력 및 일용할 성구 크롤링
def index(request):
    logger.info("INFO 레벨로 출력")

    tmr = datetime.date.today() + datetime.timedelta(1)
    t_day = datetime.date.today()
    Tomorrow = str(tmr.year) + '-' + str(tmr.month).zfill(2) + '-' + str(tmr.day).zfill(2)
    RealDay = str(t_day.year) + '-' + str(t_day.month).zfill(2) + '-' + str(t_day.day).zfill(2)

    # 크롤링할 일용할 성구 범위 선택
    def date_range(start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        return dates

    # 내일이 무슨 요일인지 계산
    yyyy = tmr.year
    mm = tmr.month
    dd = tmr.day
    def get_day_of_week(yyyy, mm, dd):
        days = ['월', '화', '수', '목', '금', '토', '일']
        return days[datetime.date(yyyy, mm, dd).weekday()]

    # 내일의 일용할 성구 크롤링
    y = str(t_day.year)
    m = str(t_day.month).zfill(2)
    d = str(t_day.day).zfill(2)
    target_day = y + '/' + m + '/' + d
    d_week = get_day_of_week(yyyy, mm, dd)
    dates = date_range(Tomorrow, Tomorrow)
    last_real_date = Scripture.objects.last()

    if dates[0] == last_real_date.real_date:
        pass
    else:
        url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + target_day
        r = requests.get(url)
        parser = BeautifulSoup(r.text, 'html.parser')
        scrip1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(3) > p.themeScrp')
        body1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(3) > div.bodyTxt > '
                                  'div.section > div.pGroup > p.sb')
        scrip = scrip1.text
        body = body1.text
        scrt = Scripture(scripture=scrip, bodytext=body, real_date=dates[0], d_week=d_week, create_date=timezone.now())
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