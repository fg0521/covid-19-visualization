import json
import pprint
from urllib.request import urlopen
import requests
import IPy



class Your_Pos():

    def __init__(self):
        """
        初始化
        """
        self.ip = urlopen('http://ip.42.pl/raw').read()
        self.ip = str(self.ip).strip('b')
        self.ip = eval( self.ip)

    def get_location(self):
        """
        获取位置
        :return: 城市名称
        """
        global city
        url = 'https://ip.help.bj.cn/?ip={}'.format(self.ip)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        try:
            res = requests.get(url, headers=headers)
            info = json.loads(res.text)
            city = ''
            if info["status"] == '200':
                city = info["data"][0]["city"]
            return city
        except Exception as e:
            print(e)

    def check_ip(self):
        """
        检查IP
        :return: 是否查询到
        """
        try:
            IPy.IP(self.ip)
            return True
        except Exception as e:
            print(e)
            return False

# ip = Your_Pos()
# if ip.check_ip():
#     city_name = ip.get_location()
# else:
#     city_name='湖州市'
# print(city_name)