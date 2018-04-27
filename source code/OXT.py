import os
import random
import  crypto_tools
from  DiffieHellman import  DiffieHellman
from T_set import T_set_client
import struct
from preprocess_f import database

class OXT_client:
    def __init__(self):

        self.ddh = DiffieHellman()
        k_s = os.urandom(512)
        k_t = os.urandom(512)
        k_i = os.urandom(512)#for producing private key
        k_x = os.urandom(512)#for producing private key
        k_z = os.urandom(512)#for producing private key
        self.iv = os.urandom(16)
        self.client_key ={}
        self.client_key["k_x"]=k_x
        self.client_key["k_i"] = k_i
        self.client_key["k_s"]=k_s
        self.client_key["k_z"] = k_z
        self.client_key["k_t"] = k_t


    def forServer(self,database):
        k_x = self.client_key["k_x"]
        k_i = self.client_key["k_i"]
        k_s = self.client_key["k_s"]
        k_z = self.client_key["k_z"]
        k_t = self.client_key["k_t"]
        secure_random = random.SystemRandom()
        dic = database.dic
        B = len(dic) ** 2
        l = len(database.file_list) ** 3  # TBD
        X_set = set()
        T = {}
        # ("yes2")

        for word in dic:
            t = []
            k_e = crypto_tools.prf_256(k_s, word)  # because aes only accept 256 bit
            array = [file for file in dic[word]]
            counter = 0

            while len(array) != 0:
                file = secure_random.choice(array)

                #   (file)
                array.remove(file)
                index = database.get_file_index(file)
                x_ind = self.ddh.genPrivateKey(k_i, str(index))

                # construct a blinded value
                z = self.ddh.genPrivateKey(k_z, word + str(counter))
                z_inv = crypto_tools.modinv(z, self.ddh.prime)
                y = (x_ind * z_inv) % self.ddh.prime

                y_s = str(y)
                y_bs = bytes(y_s, "utf-8")

                e = crypto_tools.enc(k_e, self.iv, str(index))

                element = struct.pack("H", len(y_bs)) + y_bs + e

                t.append(element)

                ####construct xset
                prvk = self.ddh.genPrivateKey(k_x, word)
                x_tag = self.ddh.genSecret(x_ind, self.ddh.genPublicKey(prvk))
                # print(pow(self.ddh.genPublicKey(prvk), x_ind, self.ddh.prime_p)==x_tag)
                X_set.add(x_tag)

                counter = counter + 1

            T[word] = t

        self.EDD = T_set_client(B, l, k_t)

        return   OXT_server(self.EDD.forServer(T), X_set,self.iv, self.ddh)


    def get_stag(self,w):
        stag = self.EDD.get_tag(self.client_key["k_t"], w)
        return stag




    def get_tokens(self,w,n):
        xtoken = [[0 for x in range(len(w))] for y in range(n)]
        for c in range(n):
            for i in range(1, len(w)):
                x1 = self.ddh.genPrivateKey(self.client_key["k_z"], w[0] + str(c))
                x2 = self.ddh.genPrivateKey(self.client_key["k_x"], w[i])
                x3 = self.ddh.genPublicKey(x1)
                xtoken[c][i] = self.ddh.genSecret(x2, x3)
        return  xtoken

    def get_k_e(self,w):
        k_e = crypto_tools.prf_256(self.client_key["k_s"], w)
        return  k_e

    def get_files(self,E,k_e):
        index = set()
        for en in E:
            index.add(crypto_tools.dec(k_e, self.iv, en))
        files = set()
        for item in index:
            ind = item.decode("utf-8")
            files.add(int(ind))

        return files




    def search(self, w, server):
        self.iv = os.urandom(16)
        stag = self.get_stag(w[0])
        t = self.EDD.retrive(stag, server.EDD_server)
        xtoken = self.get_tokens(w, len(t))
        k_e = self.get_k_e(w[0])
        files = server.search(xtoken,stag,len(w),k_e)
        return files



class OXT_server:
       def __init__(self,t_set_server, X_set,iv,ddh):
           self.EDD_server = t_set_server
           self.X_set = X_set
           self.iv = iv
           self.ddh = ddh


       def get_t(self, stag):
           t = self.EDD_server.retrive(stag)
           return  t





       def search(self, xtoken, stag, len_w):
           t = self.get_t(stag)
           C = len(t)
           E = set()
           for item in t:
               (l,) = struct.unpack("H", item[:2])
               y_bs = item[2:2 + l]
               e = item[2 + l:]
               y_s = y_bs.decode("utf-8")
               y = int(y_s)
               count = 0
               c = t.index(item)
               for i in range(1, len_w):
                   if (pow(xtoken[c][i], y, self.ddh.prime_p) in self.X_set):
                       count = count + 1

               if count == len_w - 1:
                   E.add(e)
           return  E

            # index = set()
           # for en in E:
           #   index.add(crypto_tools.dec(k_e, self.iv, en))
           # files = set()
           # for item in index:
           #     ind = item.decode("utf-8")
           #     files.add(int(ind))
           #
           # return files