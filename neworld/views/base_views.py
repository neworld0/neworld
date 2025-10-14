# neworld/views/base_views.py  (REPLACE WHOLE FILE)
from django.shortcuts import render
from neworld.models import Scripture
from django.utils import timezone
from bs4 import BeautifulSoup
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import datetime
from neworld.lib import get_number_of_week, date_range, date_range_for_crawling, get_day_of_week

logger = logging.getLogger('neworld')

# requests 세션 생성 (재시도 + 백오프)
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
session.mount('http://', adapter)

# index 페이지 출력 및 일용할 성구 크롤링


def index(request):
    logger.info("INFO 레벨로 출력")

    t_day = datetime.date.today()
    Today = f"{t_day.year}-{str(t_day.month).zfill(2)}-{str(t_day.day).zfill(2)}"
    seventhday = t_day + datetime.timedelta(7)
    Seventh_day = f"{seventhday.year}-{str(seventhday.month).zfill(2)}-{str(seventhday.day).zfill(2)}"

    # DB에 기록할 날짜 리스트 (오늘 ~ 7일 뒤)
    date_range_RealDay = date_range(Today, Seventh_day)

    # 오늘 데이터가 없으면 오늘부터 7일치 크롤링해서 채움
    try:
        Scripture.objects.get(real_date=Today)
    except Scripture.DoesNotExist:
        for i in range(len(date_range_RealDay)):
            # 실제 크롤링은 '하루 뒤 페이지'를 기준으로 함
            crawl_day = t_day + datetime.timedelta(i + 1)
            url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + \
                crawl_day.strftime('%Y/%m/%d')
            try:
                r = session.get(url, timeout=10)
                parser = BeautifulSoup(r.text, 'html.parser')
                scrip1 = parser.select_one(
                    '#dailyText > div.articlePositioner > div:nth-child(1) > p.themeScrp')
                body1 = parser.select_one(
                    '#dailyText > div.articlePositioner > div:nth-child(1) > div.bodyTxt > p.sb')
                scrip_text = scrip1.text if scrip1 else "데이터 준비 중"
                body_text = body1.text if body1 else "데이터 준비 중"
            except Exception as e:
                logger.error(f"크롤링 오류: {e}")
                scrip_text = "데이터 준비 중"
                body_text = "데이터 준비 중"

            target_day = t_day + datetime.timedelta(i)
            yyyy, mm, dd = target_day.year, target_day.month, target_day.day
            t_week = get_day_of_week(yyyy, mm, dd)

            Scripture(
                scripture=scrip_text,
                bodytext=body_text,
                real_date=date_range_RealDay[i],
                d_week=t_week,
                create_date=timezone.now()
            ).save()

    # 오늘 날짜의 성구 가져오기
    scripture1 = Scripture.objects.get(real_date=Today)
    context = {
        'today_html': scripture1.real_date,
        'day_of_week_html': scripture1.d_week,
        'scripture_html': scripture1.scripture,
        'bodyText_html': scripture1.bodytext
    }
    return render(request, 'neworld/index.html', context)
