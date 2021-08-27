import cgi, os, html_sanitizer, requests, sys, glob
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def parser():
    t = datetime.today()+timedelta(1)
    y = str(t.year)
    m = str(t.month).zfill(2)
    d = str(t.day).zfill(2)
    today = y+'/'+m+'/'+d
    url = 'https://wol.jw.org/ko/wol/h/r8/lp-ko/'+ today
    r = requests.get(url)
    parser = BeautifulSoup(r.text, 'html.parser')
    return parser

def getDir():
    root = 'neworld/data'
    dirStr = ''
    files = os.listdir(root)
    files_sorted = sorted(files)
    for entry in files_sorted:
        if os.path.isdir(os.path.join(root, entry)):
            dirStr = dirStr + '<a style="display:inline" href="meditation.py?id={directory}">   {directory}   <font color=gray>|</a>'.format(directory=entry)
    return dirStr

# os.scandir(root)를 사용한 method : 이것은 결과 값으로 list가 아니고 iterator를 반환한다.
# def getDir():
#     root = 'data'
#     dirStr = ''
#     with os.scandir(root) as entries:
#         for entry in entries:
#             if entry.is_dir():
#                 dirStr = dirStr + '<li><a href="meditation.py?id={directory}">{directory}</a></li>'.format(directory=entry.name)
#     return dirStr

def getDateList():
    sanitizer = html_sanitizer.Sanitizer()
    form = cgi.FieldStorage()
    Id = form["id"].value       # Id = 'Jeonghun\'s_Meditation/2021-07-13'
    pageId = Id[:-10]
    root = 'neworld/data/'+pageId+'*'
    files = glob.glob(root)
    listStr = ''
    for item in files:
        item = sanitizer.sanitize(item)
        i = item[5:]
        link = i.replace("\\", "/")
        list = link[-10:]
        listStr = listStr + '<li><a href="personal_meditation_list.py?id={page}">{name}</a></li>'.format(page=link, name=list)
    return listStr

def getPersonalList():
    sanitizer = html_sanitizer.Sanitizer()
    form = cgi.FieldStorage()
    pageId = form["id"].value
    root = 'neworld/data/'+pageId
    files = os.listdir(root)
    listStr = ''
    for item in files:
        item = sanitizer.sanitize(item)
        listStr = listStr + '<li><a href="personal_meditation_list.py?id={name}/{file}">{file}</a></li>'.format(name=pageId, file=item)
    return listStr

def getMeditationList():
    sanitizer = html_sanitizer.Sanitizer()
    root = 'neworld/data/'
    files = os.listdir(root)
    print(files)
    listStr = ''
    for item in files:
        item = sanitizer.sanitize(item)
        listStr = listStr + '<li><a href="personal_meditation_list.py?id={name}">{name}</a></li>'.format(name=item)
    return listStr

def getMeditation():
    sanitizer = html_sanitizer.Sanitizer()
    files = os.listdir('neworld/data')
    listStr = ''
    for item in files:
        item = sanitizer.sanitize(item)
        listStr = listStr + '<li><a href="meditation.py?id={name}">{name}</a></li>'.format(name=item)
    return listStr


def getDirCheckbox():
    sanitizer = html_sanitizer.Sanitizer()
    files = os.listdir('neworld/data')
    files_sorted = sorted(files)
    cblist = ''
    for item in files_sorted:
        item = sanitizer.sanitize(item)
        cblist = cblist + '<label><input type ="checkbox" name="name_list" value="{name}">  {name}</label><br>'.format(name=item)
    return cblist


def create(pageId):
    create = '''
        <form action="create.py" method="post">
            <input type="hidden" name="pageId" value="{}">
            <input type="submit" value="이름 생성" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>
    '''.format(pageId)
    return create

def createMeditation(pageId):
    createMeditation = '''
        <form action="create_meditation.py?={}" method="post">
            <input type="hidden" name="your_name" value="{}">
            <input type="submit" value="묵상 기록" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>
    '''.format(pageId, pageId)
    return createMeditation

def update(pageId):
    update = '''
        <form action="update.py?id={}" method="post">
            <input type="hidden" name="pageId" value="{}">
            <input type="submit" value="수정" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>
    '''.format(pageId, pageId)
    return update

def update_dir(pageId):
    update_dir = '''
        <form action="update_dir.py" method="post">
            <input type="submit" value="수정" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>'''
    return update_dir

def delete(pageId):
    delete = '''
        <form action="process_delete.py" method="post">
            <input type="hidden" name="pageId" value="{}">
            <input type="submit" value="삭제" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>
    '''.format(pageId)
    return delete


def delete_dir(pageId):
    delete_dir = '''
        <form action="delete.py" method="post">
            <input type="hidden" name="pageId" value="{}">
            <input type="submit" value="이름 삭제" style="height:50px;width:100px;font-size:100%;font-weight:bold;">
        </form>
    '''.format(pageId)
    return delete_dir
