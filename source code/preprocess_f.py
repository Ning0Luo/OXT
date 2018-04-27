#!/usr/bin/python3

import nltk
import os


# nltk.download('punkt')


class database:
    def __init__(self) :
        self.db=[]
        self.words_set=set()
        self.dic  = {}
        self.file_list=[]

    def preprocess_fie(self,filename):
        f = open(filename, "r")
        words = set()
        for line in f:
            sentences = nltk.sent_tokenize(line)
            for sentence in sentences:
                words = words.union(nltk.word_tokenize(sentence))
        return words

    def addfile(self, filename):
        self.file_list.append(filename)
        pair =[filename, self.preprocess_fie(filename)]
        self.db.append(pair)
        words=self.preprocess_fie(filename)
        self.words_set=self.words_set.union(words)
        for word in words:
            if word in self.dic:
                self.dic[word].append(filename)
            else:
                self.dic[word]=[filename]

    def scan_dir(self, dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".txt"):
                    self.addfile(dir+"/"+file)



    def get_file_index(self,file):
        return  self.file_list.index(file)



