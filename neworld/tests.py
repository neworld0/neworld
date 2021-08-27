from django.test import TestCase

from django.utils import timezone
from neworld import Scripture
import requests, os, django
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neworld.settings")
django.setup()

day = datetime.today()
RealDay = str(day.year) + '-' + str(day.month).zfill(2) + '-' + str(day.day).zfill(2)

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates

if __name__=='__main__':
    dates = date_range("2021-01-01", "2021-12-31")
    for i in dates:
        url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/' + dates[i]
        r = requests.get(url)
        parser = BeautifulSoup(r.text, 'html.parser')
        s = parser.find_all('p', {'class': 'themeScrp'})
        scrip = s[0].text
        bt = parser.find_all('div', {'class': 'bodyTxt'})
        body = bt[0].text
        Scripture(scripture=scrip, bodytext=body, real_date=dates[i], create_date=timezone.now()).save()

