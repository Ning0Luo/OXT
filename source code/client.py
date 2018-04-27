#!/usr/local/bin/python3
# client.py

import socket
import  pickle
from preprocess_f import database
from OXT import OXT_client
import os
import sys


class Xtoken:
    def __init__(self,xtoken):
        self.x = xtoken
    def xtoken(self):
        return self.x



class client:

    def __init__(self):
        self.port = 60000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.oxt = oxt = OXT_client()
        self.create_workplace("/tmp/sse_client/")

    def create_workplace(self, directory):
        self.workplace_str = directory
        if not os.path.exists(self.workplace_str):
            os.makedirs(self.workplace_str)

    def send(self,to_send, s):  # suppose s is open
        filename = self.workplace_str+"send_tmp_c.pkl"

        output = open(filename, 'wb')
        pickle.dump(to_send, output)
        output.close()
        f = open(filename, 'rb')
        l = f.read(16)
        while l:
            s.send(l)
            l = f.read(1024)
        f.close()


    def receive(self, conn):
        filename = self.workplace_str+"rec_tmp_c.pkl"

        with open(filename, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        f.close()
        pkl_file = open(filename, 'rb')
        data = pickle.load(pkl_file)
        return data

    def create_database(self,dir):
        d = database()
        d.scan_dir(dir)
        return d

    def upload_database(self,database, name):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        to_send =self.oxt.forServer(database)

        self.s.send(b"upload_database")
        self.s.recv(1024)

        self.s.send(name)
        self.send(to_send,self.s) 
        print('Done sending!')

    def retrive(self,w,name):
        # filename = "tem_rec_c"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        stag = self.oxt.get_stag(w[0])
        k_e = self.oxt.get_k_e(w[0])

        self.s.send(b'retrive_data')
        self.s.recv(1024)

        self.s.send(name)
        self.s.recv(1024)


        self.s.send(stag)
        self.s.recv(1024)

        self.s.send(b"request length")
        len_t_b=self.s.recv(1024)
       
        len_t = int(str(len_t_b,"utf-8"))


        xtoken =self.oxt.get_tokens(w,len_t)
        print("tokens produced...")

        len_w = len(w)
        len_w_b = str(len_w).encode("utf-8")
        self.s.send(len_w_b)
        self.s.recv(1024)

        self.send(xtoken,self.s)
        self.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        e_files = self.receive(self.s)
        self.s.close()
        file_index = self.oxt.get_files(e_files,k_e)
        return file_index







    def close(self):
        self.s.close()



c= client()
operation = input("operation>")

while True:
    if operation == "upload":
        print("dir> ", end='')
        database_path = input()
        print(database_path)
        database = c.create_database(database_path)
        c.upload_database(database, b"alice")

    if operation == "search":
        list = input("keywords>")
        list = list.split(",")
        index = c.retrive(list, b"alice")
        files = set()
        for i in index:
            file = database.file_list[i]
            files.add(file)
        if len(files)==0:
            print("no such files")
        else:
            print("result: ", files )

    if operation == "exit":
        break

    operation = input("operation>")

c.close()



