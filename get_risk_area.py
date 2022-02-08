# coding:utf-8
import asyncio
import csv
import datetime
import json
import os
import pprint

import aiohttp
from aiohttp import TCPConnector
from selenium.webdriver import Chrome,ChromeOptions
from time import sleep
from lxml import etree
import re
import requests
class Risk_Area():

    def __init__(self,path):
        """
        初始化
        :param path: 文件路径
        """

        self.path = path
        if os.path.exists(self.path + '/risk_areas.csv'):
            os.remove(self.path + '/risk_areas.csv')
        with open(self.path + '/risk_areas.csv', 'w') as f:
            file = csv.writer(f)
            file.writerow(['id', 'type', 'address', 'lon', 'lat'])
            f.close()
        self.risk_url = 'https://m.21jingji.com/dynamic/Zhanyi2020/riskarea?callback=jQuery341015527755580808944_1637212399299&_=1637212399300'
        self.lat_url = 'https://api.map.baidu.com/geocoding/v3?output=json&ak=wjb0GWDI3ZqXu0L9MBbfviRR8DTv0il9&address='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.pattern = re.compile(r'[(](.*?)[)]')
        self.high_risk = []
        self.mid_risk = []
        self.urls = []

    async def get_lon_lat(self, par):
        """
        :param par: 经纬度API
        :return: 带经纬度坐标
        """
        global cnt,hr,mr
        hr = {}
        mr = {}
        cnt = 0
        sem = asyncio.Semaphore(10)
        with(await sem):
            # async with是异步上下文管理器
            async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:  # 获取session
                async with session.request('GET', self.lat_url, params=par) as resp:  # 提出请求
                    try:
                        res = await resp.json(content_type='text/javascript')
                        with open(self.path + '/risk_areas.csv','a+') as f:
                            file = csv.writer(f)
                            cnt+=1
                            if res['status'] == 0:
                                if par['address'] in self.high_risk:
                                    hr[par['address']] = [res["result"]["location"]["lng"],res["result"]["location"]["lat"]]
                                    file.writerow([cnt,'high_risk',par['address'],res["result"]["location"]["lng"],res["result"]["location"]["lat"]])
                                else:
                                    file.writerow([cnt,'mid_risk', par['address'], res["result"]["location"]["lng"],
                                                   res["result"]["location"]["lat"]])
                                    mr[par['address']] = [res["result"]["location"]["lng"], res["result"]["location"]["lat"]]
                    except Exception as e:
                        print(e)

    def get_area(self):
        """
        获取高风险区域
        :return: 查询经纬度的API
        """
        def params(add):
            par = {'address': add,  # 以江苏省启东市为例
                   'ak': 'wjb0GWDI3ZqXu0L9MBbfviRR8DTv0il9',  # 百度密钥
                   'output': 'json', }
            return par
        res = requests.get(url=self.risk_url, headers=self.headers)
        result = res.text
        for i in range(len(result)):
            if result[i] == "(":
                result = result[i:]
                break
        areas = eval(result)
        for area in areas['data']:
            self.urls.append(params(area['area']))
            if area['type'] == '1':
                self.mid_risk.append(area['area'])
            elif area['type'] == '2':
                self.high_risk.append(area['area'])
            else:
                pass
        return self.urls

    def call_coroutine(self, pars):
        """
        :param pars: API列表
        :return: 启用协程
        """
        # loop = asyncio.get_event_loop()  # 获取事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.get_lon_lat(par) for par in pars]  # 把所有任务放到一个列表中
        loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
        loop.run_until_complete(asyncio.sleep(0))
        # loop.close()  # 关闭事件循环

    def save_json(self):
        """
        :return: 中高风险地区及其经纬度
        """
        with open(self.path + '/hra.json','w') as f:
            f.write(json.dumps(hr))
            f.close()
        with open(self.path + '/mra.json','w') as f:
            f.write(json.dumps(mr))
            f.close()

    def comp(self):
        """
        :return: 风险区域以及较前一天的变化
        """
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        pre = {}
        next = {}
        incre = {}
        decre = {}
        up = {}
        down = {}
        change = [['id', 'type', 'address', 'lon', 'lat']]
        cnt = 1
        with open('./疫情数据/{}/risk_areas.csv'.format(yesterday), 'r') as f:
            file = csv.reader(f)
            for line in file:
                if line[0] != 'id':
                    pre[line[2]] = [line[1], line[3], line[4]]

        with open(self.path+'/risk_areas.csv', 'r') as f:
            file = csv.reader(f)
            for line in file:
                if line[0] != 'id':
                    next[line[2]] = [line[1], line[3], line[4]]
                    change.append(line)
                    cnt += 1

        for i in next.keys():
            if i not in pre.keys():
                incre[i] = [next[i][1], next[i][2]]
                change.append([str(cnt), 'inc_' + next[i][0], i, next[i][1], next[i][2]])
                cnt += 1
            else:
                if next[i][0] != pre[i][0]:
                    if next[i][0] == 'high_risk':
                        up[i] = [next[i][1], next[i][2]]
                        change.append([str(cnt), 'up_' + next[i][0], i, next[i][1], next[i][2]])
                        cnt += 1
                    elif next[i][0] == 'mid_risk':
                        down[i] = [next[i][1], next[i][2]]
                        change.append([str(cnt), 'down_' + next[i][0], i, next[i][1], next[i][2]])
                        cnt += 1
        for j in pre.keys():
            if j not in next.keys():
                decre[j] = [pre[j][1], pre[j][2]]
                change.append([str(cnt), 'dec_' + pre[j][0], j, pre[j][1], pre[j][2]])
                cnt += 1

        with open(self.path+'/change.csv', 'w') as f:
            file = csv.writer(f)
            for line in change:
                file.writerow(line)
            f.close()

        all = {'inc': incre,
               'dec': decre,
               'up': up,
               'down': down}
        for filename, file in all.items():
            with open(self.path+'/{}.json'.format(filename), 'w') as f:
                f.write(json.dumps(file))
                f.close()