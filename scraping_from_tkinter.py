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



def show_selected(event):
    global tkinter
    global txt_url
    n = lb.curselection()   
    data=lb.get(n)        
    txt_url.delete(0,tkinter.END)
    txt_url.insert(tkinter.END,data)
    print (data)


lb = tkinter.Listbox(root,width=55)
lb.insert(0, "https://news.yahoo.co.jp/topics/top-picks")    
lb.insert(1, "https://news.yahoo.co.jp/")
lb.insert(2, "https://news.yahoo.co.jp/ranking/access/news")


lb.bind(
    "<<ListboxSelect>>",
    show_selected,
    )
lb.pack()

root.mainloop()
