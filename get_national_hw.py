import csv
import datetime
import json
import re
import time
import requests
from selenium.webdriver import Chrome,ChromeOptions

#coding=utf-8
class National_Info():

    def __init__(self,path):
        """
        初始化
        :param path: 文件路径
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            }
        self.url = ' https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=%E5%9B%BD%E5%86%85%E6%96%B0%E5%9E%8B%E8%82%BA%E7%82%8E%E6%9C%80%E6%96%B0%E5%8A%A8%E6%80%81&cb=jsonp_1639228497307_52314'
        self.filename = path + '/nation_hw.csv'

    def translate_time(self,num):
        """
        时间格式转换
        :param num:时间戳格式时间
        :return: XX-XX-XX格式时间
        """
        timeStamp = int(num)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y{}%m{}%d".format('-', '-'), timeArray)
        return otherStyleTime

    def get_nation(self):
        """
        获取全国热点新闻
        :return: 保存到本地
        """
        try:
            res = requests.get(self.url)
            result = res.text
            null = None
            for i in range(len(result)):
                if result[i] == '(':
                    result = result[i + 1:-1]
                    result = eval(result)
                    break
            info = result['Result'][0]['DisplayData']['result']['items']
            news = []
            for i in range(len(info)):
                date = self.translate_time(info[i]['eventTime'])
                content = info[i]['eventDescription']
                if info[i]['eventUrl']:
                    link = info[i]['eventUrl']
                else:
                    link = info[i]['homepageUrl']
                news.append([i + 1, date, content, link])

            with open(self.filename, 'w') as f:
                file = csv.writer(f)
                file.writerow(['id', 'date', 'content', 'link'])
                for line in news:
                    file.writerow(line)
                f.close()
        except Exception as e:
            print(e)







