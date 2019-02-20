import socketserver
import os
import sqlite3
import threading
import time

data_base_name = "/var/www/html/babyCry.db";
mutex = threading.Lock()

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        message = conn.recv(1024)
        if len(message) == 13:
            msg = message.decode('utf-8').strip()
            mutex.acquire()
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            c = dbc.cursor()
            c.execute("INSERT INTO CRYREC (DEVICE,TIME) VALUES ('"+message.decode('utf-8')+"','"+nowTime+"')");
            dbc.commit()
            mutex.release()
            print(message.decode('utf-8'))

if os.path.exists(data_base_name) == False:
    dbc = sqlite3.connect(data_base_name,check_same_thread = False)
    print("Opened database successfully");
    c = dbc.cursor()
    c.execute("CREATE TABLE CRYREC(\
       ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
       DEVICE       TEXT,\
       TIME     TEXT\
       );")
    print("Table created successfully");
    dbc.commit()
else:
    dbc = sqlite3.connect(data_base_name, check_same_thread=False)

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(('66.23.197.227', 8899, ), MyServer,bind_and_activate = False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server.serve_forever()
