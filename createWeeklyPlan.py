# coding=utf_8
from evernote.api.client import EvernoteClient
import calendar
import datetime as dt
import evernote.edam.type.ttypes as Types
import locale
import os
import textwrap

## 環境変数から値取得
NOTEBOOK_NAME = os.environ.get('NOTEBOOK_NAME')
DEV_TOKEN = os.environ.get('DEV_TOKEN')
SANDBOX = os.environ.get('SANDBOX')

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


## note作成関数の定義
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

# notebookを取得する関数の定義
def getNoteBook(noteStore):
  notebooks = noteStore.listNotebooks()
  for notebook in notebooks:
    print "Notebook: ", notebook.name
    print "NOTEBOOK_NAME: ", NOTEBOOK_NAME
    if notebook.name.decode('utf-8') == NOTEBOOK_NAME:
      return notebook

def lambda_handler(event, context):
        
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
    <en-todo checked="false"/>study
    <br/>
    <en-todo checked="false"/>fitness
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
    ''').format(date=date.strftime("%Y/%m/%d"),\
    date_1=date_1.strftime("%Y/%m/%d"),date_2=date_2.strftime("%Y/%m/%d"),\
    date_3=date_3.strftime("%Y/%m/%d"),date_4=date_4.strftime("%Y/%m/%d"),\
    date_5=date_5.strftime("%Y/%m/%d"),date_6=date_6.strftime("%Y/%m/%d"),\
    wdate=date.strftime('%a'),wdate_1=date_1.strftime('%a'),wdate_2=date_2.strftime('%a'),\
    wdate_3=date_3.strftime('%a'),wdate_4=date_4.strftime('%a'),wdate_5=date_5.strftime('%a'),\
    wdate_6=date_6.strftime('%a')).strip()
    
    print body
    
    # noteの作成
    notebook = getNoteBook(noteStore)
    if notebook:
        makeNote(DEV_TOKEN, noteStore, date.strftime("%Y/%m/%d"), body, notebook)
    else:
        makeNote(DEV_TOKEN, noteStore, data.strftime("%Y/%m/%d"), body)    

