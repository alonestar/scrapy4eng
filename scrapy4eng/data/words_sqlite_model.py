import sqlite3
import os
import time
import urllib2
import json

class WordsSqliteModel(object):
    __tableName = 'words'
    __sqliteDbDir = os.path.dirname(__file__) + '/words.db'
    __conn = None
    __cursor = None

    def __init__(self):
        # print self.__sqliteDbDir
        self.__conn = sqlite3.connect(self.__sqliteDbDir)
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.commit()
        self.__conn.close()

    def view_words(self):
        # viewSql = "select substr(add_time,0,14),count(1) from `" + self.__tableName + "` group by substr(add_time,0,14) limit 20";
        viewSql = "select substr(add_time,0,14),count(1) from `" + self.__tableName + "` where add_result=0 group by substr(add_time,0,14) limit 20"
        # viewSql = "select add_result,count(1) from `" + self.__tableName + "` group by add_result limit 20"
        # viewSql = "select * from `" + self.__tableName + "` order by add_time desc limit 20";
        return self.__cursor.execute(viewSql).fetchall()

    def view_not_report_words(self):
        viewSql = "select * from `" + self.__tableName + "` where add_result=0 order by view_count desc limit 1000";
        return self.__cursor.execute(viewSql).fetchall()

    def report_words_success(self, words, result):
        updateParam = (result, words, words+'.')
        updateSql = "update `" + self.__tableName + "` set add_result=? where word in (?, ?)"
        return self.__cursor.execute(updateSql, updateParam)

    def replace_words(self, words):
        # viewSql = "select * from `" + self.__tableName + "` where word = '%s'" % (words)
        viewSql = 'select * from `' + self.__tableName + '` where word = ?'
        # print viewSql
        try:
            result = self.__cursor.execute(viewSql, (words, )).fetchall()

            timeNow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()));
            if len(result) > 0:
                updateParam = (timeNow, words)
                updateSql = "update `" + self.__tableName + "` set update_time=?, view_count=view_count+1 where word=? "
                self.__cursor.execute(updateSql, updateParam)
            else :
                insertParam = (words, timeNow, timeNow, 1, 0)
                insertSql = "insert into `words`(word,add_time,update_time,view_count,add_result) values(?,?,?,?,?)"
                self.__cursor.execute(insertSql, insertParam)
            self.__conn.commit()
        except:
            print words

    def add_words_2_shanbay(self, words):
        url = 'https://www.shanbay.com/bdc/vocabulary/add/batch/?words='+words+'&_=1515729320747'
        headerDataArr = {
            "Host" : "www.shanbay.com",
            "Connection" : "keep-alive",
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With" : "XMLHttpRequest",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer" : "https://www.shanbay.com/bdc/vocabulary/add/batch/",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9",
            "Cookie" : "__utmc=183787513; __utmz=183787513.1515667332.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.455628750.1515667332; captcha_needed=True; language_code=zh-CN; __utma=183787513.455628750.1515667332.1515725310.1515728260.3; csrftoken=0KG2Jm3Bc3ssH3o6MGn5zQcOZk46mpm1; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vYmlsZV8xNTliNDQ4OWNjIiwiZGV2aWNlIjowLCJpc19zdGFmZiI6ZmFsc2UsImlkIjoxMDAyNzA3NTMsImV4cCI6MTUxNjU5MjI5OX0.-Wa3DeyBn-s57Hk7mFJyb6pLXDP4a50s1478mS4gs0s; sessionid=\".eJyrVopPLC3JiC8tTi2KT0pMzk7NS1GyUkrOz83Nz9MDS0FFi_V885Myc1J98tMz85ygKnWQtWcCdRoaGBiZG5ibGtcCAPu-IAk:1eZqAd:V_bMHKXV79jO4atEWGOpL0eVE3s\"; userid=100270753; __utmb=183787513.9.10.1515728260",
        };
        request = urllib2.Request(url)
        for headerDataKey, headerDataValue in headerDataArr.items():
            request.add_header(headerDataKey, headerDataValue)
        response = urllib2.urlopen(request)
        result = response.read()
        jsonRes = json.loads(result)
        if None!=jsonRes:
            return jsonRes
        else:
            return []