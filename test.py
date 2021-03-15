# coding=utf_8
from evernote.api.client import EvernoteClient
import calendar
import datetime as dt
import evernote.edam.type.ttypes as Types
import locale
import textwrap

## 変数の定義
# notebook名
NOTEBOOK_NAME = "test notebook"
NOTEBOOK_GUID = ""

# token
dev_token = "put your token"

# 日付と曜日
#locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
date = dt.date.today()
date_1 = date + dt.timedelta(days=1)
date_2 = date + dt.timedelta(days=2)
date_3 = date + dt.timedelta(days=3)
date_4 = date + dt.timedelta(days=4)
date_5 = date + dt.timedelta(days=5)
date_6 = date + dt.timedelta(days=6)

## 関数の定義
def makeNote(authToken, noteStore, noteTitle, noteBody, parentNotebook=None):

    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    ## Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

    ## parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook and hasattr(parentNotebook, 'guid'):
        ourNote.notebookGuid = parentNotebook.guid

    ## Attempt to create note in Evernote account
    try:
        note = noteStore.createNote(authToken, ourNote)
    except Errors.EDAMUserException, edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print "EDAMUserException:", edue
        return None
    except Errors.EDAMNotFoundException, ednfe:
        ## Parent Notebook GUID doesn't correspond to an actual notebook
        print "EDAMNotFoundException: Invalid parent notebook GUID"
        return None

    ## Return created note object
    return note

# Set up the NoteStore client
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
noteStore = client.get_note_store()

# Make API calls
user = userStore.getUser()
print user.username

# note本文の作成
body = textwrap.dedent('''
<h2>{date}週の目標</h2>
<en-todo checked="false"/>筋トレ
<br/>
<en-todo checked="false"/>note
<br/>

<div>{date}({wdate})</div>
<br/>
<div>{date_1}({wdate_1})</div>
<br/>
<div>{date_2}({wdate_2})</div>
<br/>
<div>{date_3}({wdate_3})</div>
<br/>
<div>{date_4}({wdate_4})</div>
<br/>
<div>{date_5}({wdate_5})</div>
<br/>
<div>{date_6}({wdate_6})</div>
<br/>
<h2>備忘録：</h2>
　note投稿(ipad, サウナ, ボート, catan, toeic, ビジネス系, news、ウイスキー、腸の話、大阪時代の話、データ分析結果)
<br/>
　pythonでfx自動取引実装のudemyを進める（スケジュール感再確認する） stay
<br/>
　仮説をたてる（noteでも英語でもpythonでもなにか） stay..
<br/>
　射精を5日に1回にする 
<br/>
　ジム いく
<br/>
　ビジネス勉強
<br/>
　画面共有アプリ
''').format(date=date.strftime("%Y/%m/%d"),\
date_1=date_1.strftime("%Y/%m/%d"),date_2=date_2.strftime("%Y/%m/%d"),\
date_3=date_3.strftime("%Y/%m/%d"),date_4=date_4.strftime("%Y/%m/%d"),\
date_5=date_5.strftime("%Y/%m/%d"),date_6=date_6.strftime("%Y/%m/%d"),\
wdate=date.strftime('%a'),wdate_1=date_1.strftime('%a'),wdate_2=date_2.strftime('%a'),\
wdate_3=date_3.strftime('%a'),wdate_4=date_4.strftime('%a'),wdate_5=date_5.strftime('%a'),\
wdate_6=date_6.strftime('%a')).strip()

print body

# noteを作成するnotebookのGUIDを取得する
notebooks = noteStore.listNotebooks()
for notebook in notebooks:
	print "Notebook: ", notebook.name
	if notebook.name == NOTEBOOK_NAME:
		makeNote(dev_token, noteStore, date.strftime("%Y/%m/%d"), body, notebook)

"""
		NOTEBOOK_GUID = notebook.guid
# notebookが存在しない場合、作成する
if NOTEBOOK_GUID == "":
	notebook = Types.Notebook()
	notebook.name = NOTEBOOK_NAME
	notebook = noteStore.createNotebook(notebook)
	NOTEBOOK_GUID = notebook.guid
"""

print(date.strftime("%Y/%m/%d"), date.strftime('%a'))
print(date_1.strftime("%Y/%m/%d"), date_1.strftime('%a'))
print(date_2.strftime("%Y/%m/%d"), date_2.strftime('%a'))
print(date_3.strftime("%Y/%m/%d"), date_3.strftime('%a'))
print(date_4.strftime("%Y/%m/%d"), date_4.strftime('%a'))
print(date_5.strftime("%Y/%m/%d"), date_5.strftime('%a'))
print(date_6.strftime("%Y/%m/%d"), date_6.strftime('%a'))

"""
note = Types.Note()
note.title = date.strftime("%Y/%m/%d")
note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Hello, world!</en-note>'
note.notebookGuid = NOTEBOOK_GUID
note = noteStore.createNote(note)
"""


