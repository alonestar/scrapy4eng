#encoding:utf8
import urllib2
import json
import enchant
import threading
import time
import nltk

def read_file(fileDir):
    fo = open(fileDir, "r")
    line = fo.read()
    fo.close()
    return line

global_wordsArr = [];
global_d = enchant.Dict("en_US")
global_wordstr = '';
def add_words(newWords):
    global global_wordstr
    newWords = newWords.lower()
    if newWords and global_d.check(newWords):
        global_wordstr = global_wordstr + newWords + " "

    if newWords and global_d.check(newWords) and newWords not in global_wordsArr:
        global_wordsArr.append(newWords)


#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################


# fword.plot(50,cumulative=True)#绘出波形图
# print(fword.hapaxes())#低频词

import nltk
#指定目录下载nltk自带的英文语料
#如果不是使用的默认路径需要执行下面的语句添加环境变量：
#vim ~/.profile
#文件末尾添加NLTK_DATA="full/path"
#source ~/.profile
nltk.download('wordnet',download_dir='/data/db/python/nltk')
# nltk.download(download_dir='/data/db/python/nltk')
#在弹出GUI界面就可以选择下载的语料了

# from nltk.book import *
# *** Introductory Examples for the NLTK Book ***
# Loading text1, ..., text9 and sent1, ..., sent9
# Type the name of the text or sentence to view it.
# Type: 'texts()' or 'sents()' to list the materials.
# text1: Moby Dick by Herman Melville 1851
# text2: Sense and Sensibility by Jane Austen 1811
# text3: The Book of Genesis
# text4: Inaugural Address Corpus
# text5: Chat Corpus
# text6: Monty Python and the Holy Grail
# text7: Wall Street Journal
# text8: Personals Corpus
# text9: The Man Who Was Thursday by G . K . Chesterton 1908
# print(text1.name)#书名
# print(text1.concordance(word="love"))#上下文
# print(text1.similar(word="very"))#相似上下文场景
# print(text1.common_contexts(words=["pretty","very"]))#相似上下文
# text4.dispersion_plot(words=['citizens','freedom','democracy'])#美国总统就职演说词汇分布图
# print(text1.collocations())#搭配
# print(type(text1))
# print(len(text1))#文本长度
# print(len(set(text1)))#词汇长度
# fword=FreqDist(text1)
# print(text1.name)#书名
# print(fword)
# voc=fword.most_common(50)#频率最高的50个字符
# fword.plot(50,cumulative=True)#绘出波形图
# print(fword.hapaxes())#低频词