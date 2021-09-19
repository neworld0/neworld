import datetime

# 오늘이 몇 주차인지 계산
def get_number_of_week():
    today = datetime.datetime.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    cal = last_monday.isocalendar()
    return cal

# 크롤링할 일용할 성구 범위 선택(RealDay 설정용)
def date_range(start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates

# 크롤링할 일용할 성구 범위 선택(크롤링 설정용)
def date_range_for_crawling(start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + datetime.timedelta(days=i)).strftime("%Y/%m/%d") for i in range((end - start).days + 1)]
    return dates

# 무슨 요일인지 계산
def get_day_of_week(yyyy, mm, dd):
    days = ['월', '화', '수', '목', '금', '토', '일']
    return days[datetime.date(yyyy, mm, dd).weekday()]

# 년, 월, 일을 입력 받아서 날짜를 생성하기
def get_date(y, m, d):
    '''y: year(4 digits)
     m: month(2 digits)
     d: day(2 digits'''
    s = f'{y:04d}-{m:02d}-{d:02d}'
    return datetime.datetime.strptime(s, '%Y-%m-%d')

# 해당 날짜가 몇 주째인지 계산하기
def get_week_no(y, m, d):
    target = get_date(y, m, d)
    firstday = target.replace(day=1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - datetime.timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + datetime.timedelta(days=6 - firstday.weekday())
    return (target - origin).days // 7 + 1
