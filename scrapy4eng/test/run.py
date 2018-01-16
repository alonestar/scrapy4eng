from scrapy4eng.data.words_sqlite_model import WordsSqliteModel



wordsObj = WordsSqliteModel()


index = 0;
for wordInfo in wordsObj.view_words():
    print wordInfo
    index+=1
    if index>10:
        break;

print wordsObj.add_words_2_shanbay('apache')

exit(-1)

allWords = wordsObj.view_not_report_words();
index = 0;
postData = None

for wordInfo in allWords:
    newWord = wordInfo[1]
    wordsResult = []
    if index % 10 == 0 or index >= len(allWords) - 1:
        wordsResult = wordsObj.add_words_2_shanbay(newWord)
        # except:
        #     print 'except'
            # time.sleep(60)
            # badWords += wordsObj.add_words_2_shanbay(newWord)
        if len(wordsResult) > 0:
            if len(wordsResult['notfound_words']) > 0:
                for notfound_words in wordsResult['notfound_words']:
                    wordsObj.report_words_success(notfound_words.lower(), 11)
                # print wordsResult
                # break
            if len(wordsResult['learning_dicts']) > 0:
                for learning_dicts in wordsResult['learning_dicts']:
                    wordsObj.report_words_success(learning_dicts['content'].lower(), 1)
        postData = newWord;
    else:
        postData = postData + '%0A' + newWord
    index += 1;

