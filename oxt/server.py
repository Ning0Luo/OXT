#!/usr/local/bin/python3
import socket
import pickle
import os
from . import oxt_impl

class Xtoken:
    def __init__(self,xtoken):
        self.x = xtoken
    def xtoken(self):
        return self.x




class server:
    def __init__(self):
        self.port = 60000
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.s.bind((self.host, self.port))  # Bind to the port
        self.s.listen(5)  # Now wait for client connection.
        self.create_workplace("/tmp/sse_server/")

    def create_workplace(self, directory):
        self.workplace_str = directory
        if not os.path.exists(self.workplace_str):
            os.makedirs(self.workplace_str)

    def listen (self) :
        while True:
            print('Server listening....')
            conn, addr = self.s.accept()  # Establish connection with client.
            print('Got connection from', addr)
            data = conn.recv(1024)
            conn.send(b'received command '+data)
            print(data)
            if data == b'upload_database':
                self.receive_database(conn)
            elif data == b'retrive_data':
                self.retrive_data(conn)

    def receive(self,filename, conn):
        filename = self.workplace_str + filename
        print(filename)
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


    def send(self, to_send,s):
        filename = self.workplace_str+"send_tmp_s.pkl"
        print(filename)
        output = open(filename, 'wb')
        pickle.dump(to_send, output)
        output.close()
        f = open(filename, 'rb')
        l = f.read(1024)
        while l:
            s.sendall(l)
            l = f.read(1024)
        f.close()

    def receive_database(self,conn):
        raw_filename = conn.recv(1024)
        filename = str(raw_filename, "utf-8")
        print(filename,"")
        data1 = self.receive(filename, conn)
        print(data1)
        print("received", filename)


    def retrive_data(self,conn):
        filename = "tmp_rec_s"

        name = conn.recv(1024)
        print(name)
        conn.send(b"your name")


        name = str(name, "utf-8")
        print(self.workplace_str+name)
        pkl_file = open(self.workplace_str+name, 'rb')
        oxt = pickle.load(pkl_file)

        stag = conn.recv(1024)
        conn.send(b"get your name and  stag")


        t = oxt.get_t(stag)
        len_t = len(t)
        len_t_b = str(len_t).encode("utf-8")

        print(conn.recv(1024))
        conn.send(len_t_b)

        len_w_b = conn.recv(1024)
        len_w = int(str(len_w_b, "utf-8"))
        conn.send(b"get your length")



        xtoken = self.receive(filename,conn)
        conn.close()
        conn, addr = self.s.accept()
        files = oxt.search(xtoken, stag, len_w)
        self.send(files,conn)
        conn.close()
        print("done!")

def run_server():
    s = server()
    s.listen()

if __name__ == "__main__":
    run_server()