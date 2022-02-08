import asyncio
import csv
import datetime
import os
import re
import time
from multiprocessing import Pool
import pkuseg
from collections import Counter
import aiohttp
import requests
from aiohttp import TCPConnector


class Wordcloud_Info():

    def __init__(self,path):
        """
        初始化
        :param path: 文件路径
        """
        global htmls
        self.path = path
        if os.path.exists(self.path + '/wb_contents.csv'):
            os.remove(self.path + '/wb_contents.csv')
        with open(self.path + '/wb_contents.csv', 'w') as f:
            file = csv.writer(f)
            file.writerow(['content'])
            f.close()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'cookie': 'SUB=_2AkMWI8ITf8NxqwJRmfsdyWngbYtwywzEieKgfzPIJRMxHRl-yT9jqkUHtRB6PaPs_MP5m6V4wHcvKtkolBWpub8V3CdH;             SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhvX_g.3acplCy2O7zonYay; SINAGLOBAL=686413323112.0806.1635733962142; ULV=1635733962154:1:1:1:686413323112.0806.1635733962142:; XSRF-TOKEN=wsa_GVWmQjdUAIeKUSSUDWaX; WBPSESS=mm07v0uQ8nV44TNSi6a9LS8gA4UTG34jw3XCWp5ifErEeMaQTr3o9-KrYhOdc3TmRe3HcApKCFrY6Rndfwmmz_SEl4O0LE3PNPhhSW380TAnCOzXl3TV2Wv56yEHJhbI',
            'referer': 'https://weibo.com/newlogin?tabtype=weibo&gid=102803600115&url=https%3A%2F%2Fweibo.com%2F'}

        htmls = []
        self.url1 = []
        for i in range(20):
            self.url1.append(
                'https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=2&group_id=102803600115&containerid=102803_ctg1_600115_-_ctg1_600115&extparam=discover%7Cnew_feed&max_id={}&count=10'.format(
                    i))

    async def get_html(self, url):
        """
        提交请求获取html内容
        :param url: 微博防疫评论API
        :return: url返回的response
        """
        # print('s')
        async with(asyncio.Semaphore(10)):# 信号量，控制协程数，防止爬的过快
            # async with是异步上下文管理器
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:  # 获取session
                try:
                    async with session.request('GET', url) as resp:  # 提出请求
                        res = await resp.json()
                        htmls.append(res)
                except Exception as e:
                    print(e)

    def call_coroutine(self):
        """
        :return: 调用协程
        """
        # loop = asyncio.get_event_loop()                 # 获取事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.get_html(url) for url in self.url1]    # 把所有任务放到一个列表中
        loop.run_until_complete(asyncio.wait(tasks))    # 激活协程
        loop.run_until_complete(asyncio.sleep(0))
        # loop.close()  # 关闭事件循环

    def parse_html(self,html,page):
        """
        :param html: 存放的response
        :param page: /
        :return: 解析html
        """
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        with open(self.path + '/wb_contents.csv', 'a+') as f:
            file = csv.writer(f)
            for each_content in html["statuses"]:
                # screen =each_content["user"]["screen_name"]
                if each_content["isLongText"]:
                    content = ''
                    mblogid = each_content["mblogid"]
                    new_url = 'https://weibo.com/ajax/statuses/longtext?id={}'.format(mblogid)
                    try:
                        new_res = requests.get(url=new_url, headers=self.headers)
                        if new_res.status_code == 200:
                            try:
                                content = new_res.json()['data']['longTextContent']
                            except:
                                content = new_res.json()['data']
                    except Exception as e:
                        print(e)

                else:
                    content = each_content["text_raw"]
                f_content = "".join(content.split())
                f_content = f_content.replace('\u200b', '')
                f_content = re.sub(pattern,'',f_content)
                if f_content:
                    # print(f_content)
                    file.writerow([f_content])
        f.close()

    def multi_process(self):
        """
        :return: 创建进程
        """
        pool = Pool(4)  # 创建进程，cpu为4核
        for i in range(len(htmls)):
            pool.apply_async(self.parse_html, args=(htmls[i], i + 1))     # 当一个进程执行完毕后会添加新的进程进去
        pool.close()    # 关闭进程池
        pool.join()     # 主进程阻塞等待子进程的退出

    def divide(self):
        """
        :return: jieba对微博评论进行分词
        """
        lexicon = ['接种疫苗', '新冠病毒', '新增病例','核酸检测','新冠肺炎','工作人员','境外输入','疑似病例',
                   '死亡病例','重症病例','追踪密切接触者','抗击肺炎疫情','肺炎疫情防控','方舱医院','健康码','行程码',
                   '无症状感染者','阳性','隔离','密切接触者','确诊病例']

        all = ''
        with open(self.path + '/wb_contents.csv','r') as f:
            reader = csv.reader(f)
            for row in reader:
                all += row[0]

        seg = pkuseg.pkuseg(user_dict=lexicon)
        text = seg.cut(all)
        with open("./static/other/stopword.txt", encoding="utf-8") as f:
            stopwords = f.read()
        new_text = []
        for w in text:
            if w not in stopwords:
                new_text.append(w)

        counter = Counter(new_text)
        result = counter.most_common()
        with open(self.path + '/div_wordcloud.csv', 'w') as f:
            file = csv.writer(f)
            file.writerow(['id','content','count'])
            no = 1
            for tuples in result:
                file.writerow([str(no), tuples[0], str(tuples[1])])
                no += 1
            f.close()

