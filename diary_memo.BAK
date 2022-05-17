from sqlite3.dbapi2 import DatabaseError, Row, paramstyle
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import signal
import sqlite3
import datetime
from contextlib import closing
import re
import requests
from bs4 import BeautifulSoup
import jaconv

import webbrowser

webbrowser.open('C:/github/Call_Python/diary_memo/diary_memo.html')


dbname = '../database.db'




def  data_print(url):
    import requests

    site = requests.get(url)
    data = BeautifulSoup(site.content, 'html.parser')
    find_data=data.find_all("a")
    #print(find_data)
    return(find_data)
    
def diary_world(request):
    print(request.params)
    in_data=request.params
    date=in_data["date"]
    today = datetime.date.today()
    if date =="":
        now = datetime.datetime.now()
        date = now
    name=in_data["name"]
    if name =="":
        name="未入力"
    weather=in_data["weather"]
    if weather =="":
        weather="未入力"
    kind=in_data["kind"]
    if kind =="":
        kind="未入力"

    kind = ''.join(kind.split())
    Contents=in_data["Contents"]

    print(Contents)
    Contents = ''.join(Contents.split())
    if ('<' in Contents) == True:
        return Response(str("<は許されない文字です"))
    match_word = in_data["match_word"]
    match_key = in_data["match_key"]
    if ("delkey" in in_data)==True:
        delkey=in_data["delkey"]
    else:
        delkey=""
    action =in_data["action"]
    if (Contents == "") and (action=="add"):
        return Response(str("記事が空です"))


    all_or_select=in_data["action2"]
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table users (id INTEGER PRIMARY KEY,date varchar(64), name varchar(64),
                      weather varchar(64), kind varchar(32), Contents varchar(256))'''
        #登録済でエラーしないようにごまかします
        try:
            c.execute(create_table)
        except:
            print("database already exist")
        if action=="view":
            if delkey == "表示":
                pass
        elif action == "add":#追加
            insert_sql = 'insert into users (date, name, weather, kind, Contents) values (?,?,?,?,?)'
            users = [
            (date, name, weather, kind, Contents)
            ]
            #この場合登録一件ですから、excutemanyでなくてもいいかも？
            #これはpythonでのサポート機能のようで、多量のレコードを一気に登録するときに役立つようです
            c.executemany(insert_sql, users)
        elif action == "scrape":#スクレいピング

            if (in_data["scraping_url"]==""):
                scraping_url = in_data["scrapeaction"]
            else:
                scraping_url = in_data["scraping_url"]


            if kind =="未入力":
                kind = scraping_url

            print("●●●●●●●●●●●●●●●●●●●●●●●●●")
            print(scraping_url)
            scraping_contents=data_print(scraping_url)
            Contents = str(scraping_contents)
            print(Contents)
            insert_sql = 'insert into users (date, name, weather, kind, Contents) values (?,?,?,?,?)'
            users = [
            (date, name, weather, kind, Contents)
            ]
            c.executemany(insert_sql, users)
        elif action == "delete":#削除
            #キー指定して削除する
            select_sql = 'delete  from users where id ='+ str(delkey)
            c.execute(select_sql)
            data="削除しました"
        elif action == "delall":#削除all
            select_sql = 'delete  from users'
            c.execute(select_sql)
            data="全レコード削除しました"
        else:
            pass
        #検索ワード表示
        if action == "srch":#検索
            select_sql = 'select * from users where Contents like '+'"%'+str(match_word)+'%"'
        elif action == "count":#検索
            select_sql =  'select id,date,(length(Contents) - length(replace(Contents, '+'\''+str(match_word)+'\''+', \'\'))) / length('+'\''+str(match_word)+'\''+') as cnt from users'
        elif action == "today":#検索
            select_sql = 'select * from users where date like '+'"%'+str(today)+'%"'
        elif action == "keyview":#指定キー表示
            select_sql = 'select * from users where id ='+ str(match_key)
        elif action == "lastview":#最後キー表示
            select_sql = 'select * from users where id in ( select max( id ) from users )'
        elif action == "kindview":#種類検索
            print(kind)
            select_sql = 'select * from users where kind like '+ '"%'+str(kind)+'%"'
        else:
        #全レコード表示
            select_sql = 'select * from users'
        data=[]
        print (select_sql )
        try:
            data.append("<table border =\"3\">")
            for row in c.execute(select_sql):
                if all_or_select == "select":
                    row=row[:5]
                print("row=")
                print(row)
                data.append("<tbody><tr><td>")
                data.append(row)
                data.append("</tbody></tr></td>")
                #ブラウザに改行を送付
                data.append("<br>")
                data.append("</td></tr>")
            conn.commit()
            print(str(data))
        except:
            print("data not found")
    if action == "scrape":        
        return Response(str(Contents))
    else:
        return Response(str(data))


    #実行処理  python サーバーを立てています
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    with Configurator() as config:
        config.add_route('diary', '/')
        config.add_view(diary_world, route_name='diary',renderer="jsonp")
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
