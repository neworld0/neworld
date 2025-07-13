from django.shortcuts import render
from neworld.models import Scripture
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
import datetime
from neworld.lib import get_number_of_week, date_range, date_range_for_crawling, get_day_of_week

logger = logging.getLogger('neworld')

def index(request):
    logger.info("INFO 레벨로 출력")

    t_day = datetime.date.today()
    Today = str(t_day.year) + '-' + str(t_day.month).zfill(2) + '-' + str(t_day.day).zfill(2)
    seventhday = t_day + datetime.timedelta(7)
    Seventh_day = str(seventhday.year) + '-' + str(seventhday.month).zfill(2) + '-' + str(seventhday.day).zfill(2)

    # DB에 실제로 기록할 날짜 리스트
    date_range_RealDay = date_range(Today, Seventh_day)

    try:
        # 오늘 날짜의 성구가 이미 있는지 확인
        Scripture.objects.get(real_date=Today)
    except Scripture.DoesNotExist:
        # 오늘 데이터가 없으면 오늘부터 다시 크롤링
        d_week = []
        for i in range(len(date_range_RealDay)):
            crawl_day = t_day + datetime.timedelta(i + 1)
            url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + crawl_day.strftime('%Y/%m/%d')
            r = requests.get(url)
            parser = BeautifulSoup(r.text, 'html.parser')
            scrip1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(1) > p.themeScrp')
            body1 = parser.select_one('#dailyText > div.articlePositioner > div:nth-child(1) > div.bodyTxt > p.sb')

            scrip_text = scrip1.text if scrip1 else "데이터 준비 중"
            body_text = body1.text if body1 else "데이터 준비 중"

            target_day = t_day + datetime.timedelta(i)
            yyyy, mm, dd = target_day.year, target_day.month, target_day.day
            t_week = get_day_of_week(yyyy, mm, dd)
            d_week.append(t_week)

            scrt = Scripture(
                scripture=scrip_text,
                bodytext=body_text,
                real_date=date_range_RealDay[i],
                d_week=t_week,
                create_date=timezone.now()
            )
            scrt.save()

    # 오늘 날짜의 성구 가져오기
    scripture1 = Scripture.objects.get(real_date=Today)
    title = scripture1.real_date
    day_of_week = scripture1.d_week
    scripture = scripture1.scripture
    bodyText = scripture1.bodytext

    context = {
        'today_html': title,
        'day_of_week_html': day_of_week,
        'scripture_html': scripture,
        'bodyText_html': bodyText
    }
    return render(request, 'neworld/index.html', context)
