from scrapy4eng.data.words_sqlite_model import WordsSqliteModel
from scrapy4eng.data.dict_eng import DictEng
# from ..data.words_sqlite_model import WordsSqliteModel
from nltk.corpus import wordnet

dictEngObj = DictEng()
wordsObj = WordsSqliteModel()

for wordInfo in wordsObj.view_words():
    print wordInfo
# print wordsObj.add_words_2_shanbay('apache')

# exit(-1)

allWords = wordsObj.view_not_report_words();
index = 0;
postData = ''

for wordInfo in allWords:
    newWord = wordInfo[1]
    wordsResult = []
    index += 1;

    print "1000|%d"%(index)
    if not dictEngObj.isEnglishWord(newWord):
        wordsObj.report_words_success(newWord, 12)
        newWord = ''

    if index % 10 == 0 or index >= len(allWords):
        # print index
        postData = postData + '%0A' + newWord
        try:
            wordsResult = wordsObj.add_words_2_shanbay(postData)
        except:
            # print postData
            postData = '';
            continue
        # except:
        #     print 'except'
        # time.sleep(60)
        # badWords += wordsObj.add_words_2_shanbay(newWord)
        if len(wordsResult) > 0:
            for updateWord in postData.split('%0A'):
                wordsObj.report_words_success(updateWord.lower(), 1)
            if len(wordsResult['notfound_words']) > 0:
                for notfound_words in wordsResult['notfound_words']:
                    wordsObj.report_words_success(notfound_words.lower(), 11)
                    # print 'not found ' + notfound_words.lower()
            if len(wordsResult['learning_dicts']) > 0:
                for learning_dicts in wordsResult['learning_dicts']:
                    wordsObj.report_words_success(learning_dicts['content'].lower(), 1)
                    # print 'found ' + learning_dicts['content'].lower()

        postData = '';
    else:
        postData = postData + '%0A' + newWord

print 'success!'
