from django.shortcuts import render
from neworld.models import Scripture
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
import datetime
from neworld.lib import get_number_of_week, date_range, date_range_for_crawling, get_day_of_week, get_week_no

logger = logging.getLogger('neworld')

# index 페이지 출력 및 일용할 성구 크롤링
def index(request):
    logger.info("INFO 레벨로 출력")

    cal = get_number_of_week()
    this_week = cal[1]
    tmr = datetime.date.today() + datetime.timedelta(1)
    t_day = datetime.date.today()
    thirdday = datetime.date.today() + datetime.timedelta(3)
    seventhday = datetime.date.today() + datetime.timedelta(7)
    Tomorrow = str(tmr.year) + '-' + str(tmr.month).zfill(2) + '-' + str(tmr.day).zfill(2)
    Third_day = str(thirdday.year) + '-' + str(thirdday.month).zfill(2) + '-' + str(thirdday.day).zfill(2)
    Seventh_day = str(seventhday.year) + '-' + str(seventhday.month).zfill(2) + '-' + str(seventhday.day).zfill(2)
    RealDay = str(t_day.year) + '-' + str(t_day.month).zfill(2) + '-' + str(t_day.day).zfill(2)

    # 3일 일용할 성구 크롤링
#    date_range_crawling = date_range_for_crawling(Tomorrow, Third_day)
    date_range_crawling = date_range_for_crawling(Tomorrow, Seventh_day)
#    date_range_RealDay = date_range(Tomorrow, Third_day)
    date_range_RealDay = date_range(Tomorrow, Seventh_day)
    last_real_date = Scripture.objects.last()
    last_real_day = datetime.datetime.strptime(last_real_date.real_date, "%Y-%m-%d")
    tmr_day = datetime.datetime.strptime(Tomorrow, "%Y-%m-%d")
    # y1 = last_real_day.year
    # m1 = last_real_day.month
    # d1 = last_real_day.day
    # n = datetime.datetime(y1, m1, d1)
    # last_n_week = n.isocalendar()
    # if last_n_week[1] >= this_week and d1 >= tmr.day:
    if last_real_day >= tmr_day:
        pass
    else:
        d_week = []
        for i in range(len(date_range_crawling)):
            url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + date_range_crawling[i]
            r = requests.get(url)
            parser = BeautifulSoup(r.text, 'html.parser')
            scrip1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(2) > p.themeScrp')
            body1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(2) > div.bodyTxt > '
                                      'div.section > div.pGroup > p.sb')
            target_day = datetime.date.today() + datetime.timedelta(1+i)
            yyyy = target_day.year
            mm = target_day.month
            dd = target_day.day
            t_week = get_day_of_week(yyyy, mm, dd)
            d_week.append(t_week)
            scrip = scrip1.text
            body = body1.text
            scrt = Scripture(scripture=scrip, bodytext=body, real_date=date_range_RealDay[i], d_week=d_week[i], create_date=timezone.now())
            scrt.save()
    scripture1 = Scripture.objects.get(real_date=RealDay)
    title = scripture1.real_date
    day_of_week = scripture1.d_week
    scripture = scripture1.scripture
    bodyText = scripture1.bodytext
    context = {'today_html': title,
               'day_of_week_html': day_of_week,
               'scripture_html': scripture,
               'bodyText_html': bodyText}
    return render(request, 'neworld/index.html', context)
