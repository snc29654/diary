from sqlite3.dbapi2 import Row
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import signal
import sqlite3
from contextlib import closing
import re
dbname = 'database.db'
def diary_world(request):
    print(request.params)
    in_data=request.params
    date=in_data["date"]
    name=in_data["name"]
    weather=in_data["weather"]
    kind=in_data["kind"]
    Contents=in_data["Contents"]
    print(Contents)
    Contents = ''.join(Contents.split())
    match_word = in_data["match_word"]
    if ("delkey" in in_data)==True:
        delkey=in_data["delkey"]
    else:
        delkey=""
    action =in_data["action"]
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
        elif action == "delete":#削除
                #キー指定して削除する
                select_sql = 'delete  from users where id ='+ str(delkey)
                c.execute(select_sql)
                data="削除しました"
        else:
            pass
        #検索レコード表示
        if action == "srch":#検索
            select_sql = 'select * from users where Contents like '+'"%'+str(match_word)+'%"'
        else:
        #全レコード表示
            select_sql = 'select * from users'
        data=[]
        print (select_sql )
        try:
            data.append("<table border =\"3\">")
            for row in c.execute(select_sql):
                #print(row)
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