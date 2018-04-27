import socket
import  pickle

def send(tosend,s) :
    filename = "send_tmp.pkl"
    output = open(filename, 'wb')
    output.close()
    f = open(filename, 'rb')
    l = f.read(1024)
    while l:
        s.sendall(l)
        l = f.read(1024)
    f.close()

def receive(socket):
    filename = "tmp_rec"
    with open(filename, 'wb') as f:
        print('file opened')
        while True:
            data = socket.recv(1024)
            if not data:
                break
            f.write(data)
    f.close()
    print('Successfully get the file')
    pkl_file = open(filename, 'rb')
    data = pickle.load(pkl_file)
    return data