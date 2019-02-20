#coding=utf-8
#pip install pyecharts -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
import os
import sqlite3
import threading
import time
from pyecharts import Scatter
from pyecharts import Pie,Timeline
from pyecharts import Bar
import web

urls = (
    '/show', 'ShowClass',
)
class ShowClass:
    def GET(self):
        data = web.input(date=None)
        show(data.date)
        return "<html><iframe width=100% height=100% src=http://1.iloveyov.com:1342/bar01.html></iframe></html>"

def show(thisday):
    print(thisday)
    data_base_name = "/var/www/html/babyCry.db";
    dbc = sqlite3.connect(data_base_name, check_same_thread=False)
    c = dbc.cursor()
    data = c.execute("select * from CRYREC");
    y_data = [0]*24
    x_data = range(0,24)
    for row in data:
        day = row[2].split(' ')[0]
        hour = int(list(row[2].split(' ')[1])[0])*10+int(list(row[2].split(' ')[1])[1])
        for i in range(0,24):
            if thisday == day and hour == i:
                y_data[i]+=1
    print y_data
    dbc.close()

    bar = Bar("宝宝的动静轨迹",thisday)
    kwargs = dict(name = '柱形图',x_axis = x_data,y_axis = y_data)
    bar.add(**kwargs)
    bar.render('/var/www/html/bar01.html')

#show("2019-02-19")

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
