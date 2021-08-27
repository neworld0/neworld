from django.shortcuts import render
from datetime import datetime

from ..models import Scripture

import logging

logger = logging.getLogger('neworld')

# index 페이지 생성
def index(request):

    logger.info("INFO 레벨로 출력")
    day = datetime.today()
    RealDay = str(day.year) + '-' + str(day.month).zfill(2) + '-' + str(day.day).zfill(2)
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

