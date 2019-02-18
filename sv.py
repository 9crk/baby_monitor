import socketserver
import os
import sqlite3
import threading
import time

data_base_name = "babyCry.db";
mutex = threading.Lock()
count = 0
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        global count
        conn = self.request
        message = conn.recv(1024)
        if len(message) == 13:
            #msg = message.decode('utf-8')
            mutex.acquire()
            count = count+1
            nowTime = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
            c = dbc.cursor()
            c.execute("INSERT INTO CRYREC (ID,DEVICE,TIME) VALUES ("+str(count)+",'"+message.decode('utf-8')+"','"+nowTime+"')");
            dbc.commit()
            mutex.release()
            print(message.decode('utf-8'))

if os.path.exists(data_base_name) == False:
    dbc = sqlite3.connect(data_base_name,check_same_thread = False)
    print("Opened database successfully");
    c = dbc.cursor()
    c.execute("CREATE TABLE CRYREC(\
       ID INT PRIMARY KEY     NOT NULL,\
       DEVICE       TEXT,\
       TIME     TEXT\
       );")
    print("Table created successfully");
    dbc.commit()
else:
    dbc = sqlite3.connect(data_base_name, check_same_thread=False)

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(('66.23.197.227', 8899, ), MyServer)
    server.serve_forever()
