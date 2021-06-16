############################################
from tkinter.scrolledtext import ScrolledText
import datetime
import tkinter
import sys
from tkinter import messagebox
import sqlite3
from contextlib import closing

import requests
from bs4 import BeautifulSoup

from tkinter import ttk
dbname = '../database.db'

fontsize =10

root = tkinter.Tk()


def getTextInput():
    result=textExample.get("1.0","end")
    print(result)



textExample=ScrolledText(root, height=40,width=80, wrap=tkinter.CHAR)
textExample.pack()
textExample.place(x=90, y=70)


btnRead=tkinter.Button(root, height=1, width=10, text="Clear", 
                    command=getTextInput)


def btn_click6():
    global fontsize
    fontsize = fontsize + 1
    textExample.configure(font=("Courier", fontsize))
    
def btn_click7():
    global fontsize
    fontsize = fontsize - 1
    textExample.configure(font=("Courier", fontsize))


#検索
def btn_click():
    textExample.configure(font=("Courier", 10))

    data_exist =0

    #get_data =txt2.get()

    match_word = get_data
    if match_word=="":
        return

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'select * from users where mean like '+'"%'+str(match_word)+'%"'

        data=[]
        print (select_sql )
        try:

            for row in c.execute(select_sql):
                data_exist = 1;
                print(row)
                print(type(row))
                text = "-".join(map(str, row))
                print(text)
                print(type(text))
                data.append(text)
                text2="".join(map(str, data))
                data.append("----------------------------------------------------------------\n")
            conn.commit()

        except:

            print("data exception")

    
    textExample.delete("1.0",tkinter.END)

    textExample.insert(tkinter.END,text2)

    return data_exist

def btn_click10():
    textExample.configure(font=("Courier", 10))

    data_exist =0

    #get_data =txt2.get()

    match_word = ""

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'select * from users where mean like '+'"%'+str(match_word)+'%"'

        data=[]
        print (select_sql )
        try:

            for row in c.execute(select_sql):
                data_exist = 1;
                print(row)
                print(type(row))
                text = "-".join(map(str, row))
                if combovalue =='header':
                    text=text[:80]

                print(text)
                print(type(text))
                data.append(text)
                text2="".join(map(str, data))
                data.append("----------------------------------------------------------------\n")
            conn.commit()

        except:

            print("data exception")

    
    textExample.delete("1.0",tkinter.END)

    textExample.insert(tkinter.END,text2)

    return data_exist


#指定キー表示
def btn_click8():
    textExample.configure(font=("Courier", 10))

    data_exist =0

    get_data =txt.get()

    match_word = get_data

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'select * from users where item_id like '+'"%'+str(match_word)+'%"'

        data=[]
        print (select_sql )
        try:

            for row in c.execute(select_sql):
                data_exist = 1;
                print(row)
                print(type(row))
                text = "-".join(map(str, row))
                print(text)
                print(type(text))
                data.append(text)
                text2="".join(map(str, data))
                data.append("----------------------------------------------------------------\n")
            conn.commit()

        except:

            print("data exception")

    
    textExample.delete("1.0",tkinter.END)

    textExample.insert(tkinter.END,text2)

    return data_exist
#追加
def btn_click2():
    txt.delete(0,tkinter.END)
    now = datetime.datetime.now()
    txt.insert(tkinter.END,now)
    txt.insert(tkinter.END,"\n")

    get_data =txt.get()
    get_mean =textExample.get('1.0', 'end')


    #if btn_click() == 0:

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table users (id INTEGER PRIMARY KEY,date varchar(64), name varchar(64),
                      weather varchar(64), kind varchar(32), Contents varchar(256))'''
        #登録済でエラーしないようにごまかします
        try:
            c.execute(create_table)
        except:
            print("database already exist")

        insert_sql = 'insert into users (date, name, weather, kind, Contents) values (?,?,?,?,?)'
        users = [
        (get_data, get_data, get_data, get_data, get_mean)
        ]
        c.executemany(insert_sql, users)
 
        conn.commit()

def  data_print():
    import requests
    get_url =txt_url.get()

    site = requests.get(get_url)
    data = BeautifulSoup(site.text, 'html.parser')
    textExample.insert(tkinter.END,data.find_all("a"))

def btn_click2_scraping():
    txt.delete(0,tkinter.END)
    now = datetime.datetime.now()
    txt.insert(tkinter.END,now)
    txt.insert(tkinter.END,"\n")
    data_print()
    get_data =txt.get()
    get_mean =textExample.get('1.0', 'end')


    #if btn_click() == 0:
    get_date = datetime.datetime.now()
    get_name="未入力"
    get_weather="未入力"

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_sql = 'insert into users (date, name, weather, kind, Contents) values (?,?,?,?,?)'
        users = [
        (get_date, get_name,get_weather, get_data, get_mean)
        ]
        c.executemany(insert_sql, users)
        conn.commit()


#テキストボックスクリア
def btn_click3():

    textExample.delete("1.0",tkinter.END)

#キー指定削除
def btn_click4():

    get_data =txt.get()

    match_word = get_data


    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'delete from users where item_id = '+'"'+str(match_word)+'"'

        data=[]
        print (select_sql )
        try:

            for row in c.execute(select_sql):
                print(row)
                data.append(row)

            conn.commit()

        except:

            print("data not found")

#指定キー更新
def btn_click9():
    get_data =txt.get()
    match_word = get_data
    get_mean =textExample.get('1.0', 'end')


    #if btn_click() == 0:

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        insert_sql = 'update users set mean ='+'"'+str(get_mean)+'"'+ 'where item_id = '+'"'+str(match_word)+'"'
        print(insert_sql)
        c.execute(insert_sql)
        conn.commit()


def btn_click5():
    ret = messagebox.askyesno('確認', '全削除やめますか？')
    if ret == True:
        pass
    else:    
        get_data =txt.get()

        match_word = get_data


        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()
            select_sql = 'delete from users'

            data=[]
            print (select_sql )
            try:

                for row in c.execute(select_sql):
                    print(row)
                    data.append(row)

                conn.commit()

            except:

                print("data not found")

        textExample.delete("1.0",tkinter.END)

        textExample.insert(tkinter.END,"削除しました")

btn3 = tkinter.Button(root, text='入力クリア', command=btn_click3)
btn3.place(x=10, y=570)

btn11 = tkinter.Button(root, text='scraping追加', command=btn_click2_scraping)
btn11.place(x=10, y=360)

# 画面サイズ
root.geometry('1000x750')
# 画面タイトル
root.title('スクレイピング')

# ラベル
lbl = tkinter.Label(text='キー')
lbl.place(x=10, y=10)

lbl3 = tkinter.Label(text='Scraping URL')
lbl3.place(x=10, y=40)


lbl2 = tkinter.Label(text='メモ')
lbl2.place(x=10, y=70)

# テキストボックス
txt = tkinter.Entry(width=30)
txt.place(x=90, y=10)
txt.insert(tkinter.END,"")

txt_url = tkinter.Entry(width=80)
txt_url.place(x=120, y=40)
txt_url.insert(tkinter.END,"")

# 表示
root.mainloop()