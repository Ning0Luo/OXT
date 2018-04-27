import os
from . import crypto_tools
import random
from bitstring import BitArray
#key = int.from_bytes(os.urandom(256), byteorder="big")
#h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
#h.update(b"message to hash")
#h.finalize()
class T_set_client:
    def __init__(self, B,l, k_tset): #B and s are determined by N =sum(T(w)) t should be a  dictionary
        self.__k_tset = k_tset
        self.B = B
        self.l = l


    def get_tag(self,k, keyword):
        stag= crypto_tools.prf_512(k,keyword)
        return  stag

    def retrive(self,tag,t_set_server):
         return  t_set_server.retrive(tag)

    def forServer(self,T):
        free = [[x for x in range(self.l)] for y in range(self.B)]
        self.t_set = [[(0, 0) for x in range(self.l)] for y in range(self.B)]

        for word in T:
            stag = crypto_tools.prf_512(self.__k_tset, word)
            t = T[word]
            beta = 1
            i = 0
            for s in t:
                str_i = str(i)
                i = i + 1
                s = bytearray(s)
                inner = crypto_tools.prf_512(stag, str_i)
                # blk_array=bytearray(crypto_tools.hash(inner))
                h_value = crypto_tools.hash(inner)
                b = h_value[0]
                label = h_value[1:32]
                k = h_value[33:64]
                k = crypto_tools.hash_length(k, 3)
                if len(free[b]) == 0:
                    self.forServer()
                else:
                    j = random.choice(free[b])
                    free[b].remove(j)
                    if i == len(t):
                        beta = 0
                    s.insert(0, beta)
                    s_append = bytes(s)

                    value = bytes(a ^ b for a, b in zip(s_append, k))  # k's length
                    self.t_set[b][j] = (label, value)

        return T_set_server(self.t_set)


class T_set_server:
    def __init__(self, t_set):
            self.tset = t_set


    def retrive(self, tag):
        t = []
        beta = 1
        i = 0
        while beta == 1:
                str_i = str(i)
                i = i + 1
                inner = crypto_tools.prf_512(tag, str_i)
                h_value = crypto_tools.hash(inner)
                b = h_value[0]
                label = h_value[1:32]
                k = h_value[33:64]
                k = crypto_tools.hash_length(k, 3)
                for item in self.tset[b]:
                    if item[0] == label:
                        s = bytes(a ^ b for a, b in zip(item[1], k))
                        beta = s[0]
                        s = s[1:]
                        t.append(s)
                if len(t) == 0:
                     break
        return t


