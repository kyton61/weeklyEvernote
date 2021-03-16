# coding=utf_8
from evernote.api.client import EvernoteClient
import calendar
import configparser
import datetime as dt
import errno
import evernote.edam.type.ttypes as Types
import locale
import os
import textwrap

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini_path = 'config.ini'
if not os.path.exists(config_ini_path):
	raise FileNotFoundError(errno.ENOET, os.strerror(error.ENOENT), config_ini_path)
config_ini.read(config_ini_path, encoding='utf-8')

# config.iniから値取得
NOTEBOOK_NAME = config_ini['evernote']['Notebook_name']
DEV_TOKEN = config_ini['evernote']['Dev_token']
SANDBOX = config_ini['evernote']['Sandbox']

## 変数の定義
NOTEBOOK_GUID = ""
# 日付と曜日
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

# noteを作成するnotebookのGUIDを取得する
def getNotebook(noteStore):
  notebooks = noteStore.listNotebooks()
  for notebook in notebooks:
    print "Notebook: ", notebook.name
    print "NOTEBOOK_NAME: ", NOTEBOOK_NAME
    if notebook.name.decode('utf-8') == NOTEBOOK_NAME:
      return notebook

# Set up the NoteStore client
client = EvernoteClient(token=DEV_TOKEN, sandbox=SANDBOX)
noteStore = client.get_note_store()

# debug
userStore = client.get_user_store()
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


# noteの作成
notebook = getNotebook(noteStore)
if notebook:
	makeNote(DEV_TOKEN, noteStore, date.strftime("%Y/%m/%d"), body, notebook)
else:
	makeNote(DEV_TOKEN, noteStore, date.strftime("%Y/%m/%d"), body)

