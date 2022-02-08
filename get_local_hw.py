import asyncio
import csv
import datetime
import os
import re
import time
from multiprocessing import Pool
import requests
import aiohttp


class Local_Info():

    def __init__(self,path,city):
        """
        初始化
        :param path: 文件路径
        :param city: 用户IP定位城市
        """
        global htmls
        self.path = path
        if os.path.exists(self.path + '/local_hw.csv'):
            os.remove(self.path + '/local_hw.csv')
        with open(self.path + '/local_hw.csv', 'w') as f:
            file = csv.writer(f)
            file.writerow(['id', 'date', 'content', 'link'])
            f.close()
        htmls = []
        self.url2= []
        for i in range(5):
            self.url2.append(
                'http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word={}疫情&pn={}'.format(city, i * 10))

    def deal_date_again(self,date):
        """
        时间格式转换
        :param date: X年X月X日
        :return: XX年XX月XX日
        """
        s = date[:5]
        m, d = date.index('月'), date.index('日')
        if len(date[5:m]) == 1:
            s = s + '0' + date[5:m] + '月'
        else:
            s = s + date[5:m] + '月'
        if len(date[m + 1:d]) == 1:
            s = s + '0' + date[m + 1:d] + '日'
        else:
            s = s + date[m + 1:d] + '日'
        return s

    def deal_date(self,date):
        """
        时间格式转换
        :param date: 各种类型时间（X分钟前，X小时前，X月X日...）
        :return: XX-XX-XX格式时间
        """
        if '昨天' in date:
            d = datetime.date.today() - datetime.timedelta(days=1)
            comp_date = d.strftime("%Y{}%m{}%d{}").format("年","月","日")
        elif '前天' in date:
            d = datetime.date.today() - datetime.timedelta(days=2)
            comp_date = d.strftime("%Y{}%m{}%d{}").format("年","月","日")
        elif '天前' in date:
            num = re.findall("\d+", date)[0]
            d = datetime.date.today() - datetime.timedelta(days=int(num))
            comp_date = d.strftime("%Y{}%m{}%d{}").format("年","月","日")
        elif '小时前' in date or '今天' in date or '分钟前' in date:
            comp_date = time.strftime("%Y{}%m{}%d{}").format("年", "月", "日")
        elif '年' not in date:
            comp_date = time.strftime("%Y{}").format("年") + date
        else:
            comp_date = date
        if len(comp_date) < 11:
            final_date = datetime.datetime.strptime(self.deal_date_again(comp_date), '%Y年%m月%d日').strftime("%Y-%m-%d")

        else:
            final_date = datetime.datetime.strptime(comp_date, '%Y年%m月%d日').strftime("%Y-%m-%d")
        return final_date

    async def get_html(self, url):
        """
        提交请求获取html内容
        :param url: 网址
        :return: 从url中获取的response
        """
        sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快
        with(await sem):
            # async with是异步上下文管理器
            async with aiohttp.ClientSession() as session:  # 获取session

                try:
                    async with session.request('GET', url) as resp:  # 提出请求
                        # 正则匹配更快
                        res = await resp.text()
                        htmls.append(res)
                except Exception as e:
                    print(e)

    def call_coroutine(self):
        """
        :return: 调用协程
        """
        loop = asyncio.get_event_loop()                 # 获取事件循环
        tasks = [self.get_html(url) for url in self.url2]    # 把所有任务放到一个列表中
        loop.run_until_complete(asyncio.wait(tasks))    # 激活协程
        loop.run_until_complete(asyncio.sleep(0))
        # loop.close()  # 关闭事件循环

    def parse_html(self,html,page):
        """
        :param html: 保存的url的response
        :param page: 需要获取的网页页数
        :return: 解析html
        """
        com1 = re.compile('aria-label="发布于：(.*)">')    # 正则匹配
        com2 = re.compile('aria-label="标题：(.*)" data-click="')
        com3 = re.compile('class="news-title_1YtI1"><a href="(.*)" target="_blank"')
        date = re.findall(com1, html)
        title = re.findall(com2, html)
        link = re.findall(com3, html)
        with open(self.path + '/local_hw.csv','a+') as f:
            file = csv.writer(f)
            for i in range(len(title)):
                id = (page - 1) * 10 + (i + 1)
                d = self.deal_date(date[i])
                title[i] = title[i].replace(',','、')
                file.writerow([id, d, title[i], link[i]])
        f.close()

    def multi_process(self):
        """
        :return: 创建多进程
        """
        pool = Pool(4)  # 创建进程，cpu为4核
        for i in range(len(htmls)):
            pool.apply_async(self.parse_html, args=(htmls[i], i+1))     # 当一个进程执行完毕后会添加新的进程进去
        pool.close()    # 关闭进程池
        pool.join()     # 主进程阻塞等待子进程的退出
