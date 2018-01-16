import os

class DictEng(object):
    __engDictDir = os.path.dirname(__file__) + '/dict/wordsEn.txt'
    __engWords = None

    def __init__(self):
        with open(self.__engDictDir) as word_file:
            self.__engWords = set(word.strip().lower() for word in word_file)

    def isEnglishWord(self, word):
        return word.lower() in self.__engWords