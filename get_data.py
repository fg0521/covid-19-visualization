# from datetime import datetime, date
import os
import pprint
import time
import csv
import requests
from lxml import etree
import json
import pandas as pd
import datetime

class Get_data():

    def __init__(self,path):
        """
        初始化
        :param path: 文件路径
        """
        self.url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36 '
        }
        self.filename1 = path + '/china_tend.csv'
        self.filename2 = path + '/province.csv'
        self.filename3 = path + '/cities.csv'
        self.filename4 = path + '/oversea_country.csv'
        self.filename5 = path + '/continent.csv'
        self.filename6 = path + '/oversea_trend.csv'
        self.filename7 = path + '/summary.csv'

    def parse_data(self):
        """
        :return: 分析网址获取数据
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                html = etree.HTML(response.text)    # 生成HTML对象
                datas = html.xpath('//script[@type="application/json"]/text()')     # 解析数据
                datas = json.loads(datas[0])
                with open('./static/other/result.json', 'w') as file:      # 存放数据
                    file.write(json.dumps(datas))
            else:
                print('前一天的数据')
                with open('./static/other/result.json', 'r') as file:       # 如果不能获取数据则调用上次存入的文件
                    datas = json.load(file)
            return datas
        except Exception as e:
            print(e)

    def china_trend_info(self,result):
        """
        :param result: 获取的总信息
        :return: 中国疫情发展趋势
        updateDate: 日期（list）
        list: 存放累计确诊/疑似/治愈/死亡/境外输入 新增确诊/疑似/治愈/死亡/境外输入（dict形式存在在list）
        name: 存放标题 dict键
        data: 存放内容 dict值
        """

        info = result['component'][0]['trend']
        keys = ['id','date','confirmed','unconfirmed','cured','died','curConfirmRelative','unconfirmedRelative','cureRelative','diedRelative',
               'overseasInput','overseasInputRelative']
        y = str(datetime.datetime.now().year) + '.'
        with open(self.filename1,'w') as f:
            my = csv.writer(f)
            my.writerow(keys)
            id = 1
            for i in range(len(info['updateDate'])-60,len(info['updateDate'])):
                date = y + info['updateDate'][i]
                date = datetime.datetime.strptime(date, '%Y.%m.%d').strftime("%Y-%m-%d")
                each_row = [id,date,info['list'][0]['data'][i],
                            info['list'][1]['data'][i],info['list'][2]['data'][i],
                            info['list'][3]['data'][i],info['list'][4]['data'][i],
                            info['list'][5]['data'][i],info['list'][6]['data'][i],
                            info['list'][7]['data'][i],info['list'][8]['data'][i],
                            info['list'][9]['data'][i]]
                id += 1
                my.writerow(each_row)

    def province_info(self,result):
        """
        :param result: 获取的总信息
        :return: 中国各省份疫情情况
        'confirmed': 累计确诊
        'died': 累计死亡
        'crued': 累计治愈
        'relativeTime': 时间戳
        'confirmedRelative': 累计确诊增量
        'diedRelative': 累计死亡增量
        'curedRelative': 累计治愈增量
        'asymptomaticRelative': 无症状者增量
        'asymptomatic': 无症状者
        'nativeRelative': 当地新增？
        'curConfirm': 现有确诊
        'curConfirmRelative': 现有确诊增量
        'overseasInputRelative': 海外输入增量
        'icuDisable': 重症患者
        'area': 省份
        'subList': 'city': 城市
                   'confirmed': 累计确诊
                   'died': 累计死亡
                   'crued': 累计治愈
                   'confirmedRelative': 累计确诊增量
                   'asymptomaticRelative': 无症状者增量
                   'asymptomatic': 无症状者
                   'nativeRelative': 当地新增
                   'curConfirm': 现有确诊
                   'cityCode': 城市代码
        """

        info = result['component'][0]['caseList']
        keys = ['id','area','asymptomatic','asymptomaticRelative','confirmed','confirmedRelative','crued','curConfirm','curConfirmRelative','curedRelative',
                'died','diedRelative','icuDisable','nativeRelative','overseasInputRelative']
        p_id = 1
        with open(self.filename2,'w') as f:
            my = csv.writer(f)
            my.writerow(keys)
            for i in range(len(info)):
                each_provinde = []
                each_provinde.append(p_id)
                for key in keys[1:]:
                    if info[i][key] == '':
                        info[i][key] = '0'
                    each_provinde.append(info[i][key])
                my.writerow(each_provinde)
                p_id += 1

        keys2 =['id','city','confirmed','died','crued','confirmedRelative','asymptomaticRelative','asymptomatic','nativeRelative','curConfirm']
        increase = {
            '西藏':[['西藏_阿里地区','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['西藏_那曲地区','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['西藏_昌都市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['西藏_林芝市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['西藏_山南市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['西藏_日喀则市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '青海':[['青海_海西蒙古族藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['青海_玉树藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['青海_果洛藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['青海_黄南藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['青海_海南藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['青海_海东市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '吉林':[['吉林_延边朝鲜族自治州','-1','-1','-1','-1','-1','-1','-1','-1']],
            '新疆':[['新疆_阿勒泰地区','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_塔城地区','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_哈密市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_昌吉回族自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_克拉玛依市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_博尔塔拉蒙古自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_阿拉尔市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_克孜勒苏柯尔克孜自治州','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_和田地区','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_图木舒克市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_北屯市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_五家渠市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_双河市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_石河子市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_可克达拉市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_铁门关市','-1','-1','-1','-1','-1','-1','-1','-1'],
                  ['新疆_昆玉市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '甘肃': [['甘肃_嘉峪关市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '海南': [['海南_白沙黎族自治县','-1','-1','-1','-1','-1','-1','-1','-1'],
                   ['海南_五指山市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '云南': [['云南_迪庆藏族自治州','-1','-1','-1','-1','-1','-1','-1','-1']],
            '广西': [['广西_崇左市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '北京': [['北京_平谷区','-1','-1','-1','-1','-1','-1','-1','-1']],
            '山东': [['山东_莱芜市','-1','-1','-1','-1','-1','-1','-1','-1'],
                   ['山东_东营市','-1','-1','-1','-1','-1','-1','-1','-1']],
            '重庆': [['重庆_北碚区','-1','-1','-1','-1','-1','-1','-1','-1'],
                   ['重庆_南川区','-1','-1','-1','-1','-1','-1','-1','-1']],
            '广东': [['广东_云浮市','-1','-1','-1','-1','-1','-1','-1','-1']],
        }
        tab = {
            '海北州':'青海_海北藏族自治州',
            '黔东南州':'贵州_黔东南苗族侗族自治州',
            '黔南州':'贵州_黔南布依族苗族自治州',
            '黔西南州':'贵州_黔西南布依族苗族自治州',
            '毕节地区':'贵州_毕节市',
            '铜仁地区':'贵州_铜仁市',
            '吐鲁番地区':'新疆_吐鲁番市',
            '伊犁州':'新疆_伊犁哈萨克自治州',
            '阿克苏地区':'新疆_阿克苏地区',
            '喀什地区':'新疆_喀什地区',
            '临夏州':'甘肃_临夏回族自治州',
            '甘南州':'甘肃_甘南藏族自治州',
            '大兴安岭地区':'黑龙江_大兴安岭地区',
            '临高':'海南_临高县',
            '澄迈':'海南_澄迈县',
            '定安':'海南_定安县',
            '屯昌':'海南_屯昌县',
            '德宏州':'云南_德宏傣族景颇族自治州',
            '红河州':'云南_红河哈尼族彝族自治州',
            '怒江州': '云南_怒江傈僳族自治州',
            '文山': '云南_文山壮族苗族自治州',
            '楚雄州': '云南_楚雄彝族自治州',
            '大理州': '云南_大理白族自治州',
            '甘孜州': '四川_甘孜藏族自治州',
            '阿坝州': '四川_阿坝藏族羌族自治州',
            '凉山州': '四川_凉山彝族自治州',
            '湘西州': '湖南_湘西土家族苗族自治州',
            '恩施': '湖北_恩施土家族苗族自治州',
            '神农架林区': '湖北_神农架林区',
            '梁平区':'重庆_梁平县',
            '石柱县':'重庆_石柱土家族自治县',
            '武隆区':'重庆_武隆县',
            '彭水县':'重庆_彭水苗族土家族自治县',
            '酉阳县':'重庆_酉阳土家族苗族自治县',
            '秀山县':'重庆_秀山土家族苗族自治县',
        }
        special_city =[['台湾_中国属钓鱼岛', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_连江县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_金门县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_新北市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_基隆市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_台北市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_桃园市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_新竹市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_新竹县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_宜兰县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_苗栗县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_台中市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_彰化县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_南投县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_花莲县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_云林县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_嘉义市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_嘉义县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_台南市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_高雄市', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_台东县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_屏东县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['台湾_澎湖县', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_花地玛堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_花王堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_望德堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_风顺堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_大堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_嘉模堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_路凼填海区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['澳门_圣方济各堂区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_北区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_元朗区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_屯门区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_离岛区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_大埔区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_沙田区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_葵青区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_黄大仙区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_西贡区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_观塘区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_东区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_九龙城区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_湾仔区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_中西区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_油尖旺区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_深水埗区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_荃湾区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                     ['香港_南区', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]
        c_id = 1
        with open(self.filename3,'w') as f:
            my2 = csv.writer(f)
            # csv写入表头
            my2.writerow(keys2)
            # 单独添加澳门、台湾、香港
            for spec in special_city:
                my2.writerow([c_id]+spec)
                c_id += 1
            # 遍历省份
            for i in range(len(info)):
                # 添加没有记录的城市，所有数据为-1
                if info[i]['area'] in increase.keys():
                    for infos in increase[info[i]['area']]:
                        my2.writerow([c_id]+infos)
                        c_id += 1
                # 遍历城市，添加城市
                for j in range(len(info[i]['subList'])):
                    each_city = []
                    # 对城市名称进行处理,需要和js地图相符合
                    if info[i]['area'] == '上海' or info[i]['area'] =='北京' or info[i]['area'] =='天津' or info[i]['area'] =='重庆'\
                            or info[i]['subList'][j]['city'] == '境外输入' or info[i]['subList'][j]['city'] == '外来人员'\
                            or info[i]['subList'][j]['city'] == '待确认' or info[i]['subList'][j]['city'][-3:]=='自治县'\
                            or info[i]['subList'][j]['city'][-3:]=='自治州' or info[i]['subList'][j]['city']=='吉林市'\
                            or info[i]['subList'][j]['city'][-1:]=='盟':
                        if info[i]['subList'][j]['city'] in ['梁平区','石柱县','武隆区','彭水县','酉阳县','秀山县']:
                            each_city.append(tab[info[i]['subList'][j]['city']])
                        else:
                            each_city.append(info[i]['area']+ '_'+info[i]['subList'][j]['city'])
                    elif info[i]['area'] in ['青海','贵州','新疆','甘肃','黑龙江','海南','云南','四川','湖南','湖北']:
                        if info[i]['subList'][j]['city'] in tab.keys():
                            each_city.append(tab[info[i]['subList'][j]['city']])
                        else:
                            each_city.append(info[i]['area'] + '_' + info[i]['subList'][j]['city'] + "市")
                    else:
                        each_city.append(info[i]['area'] + '_' + info[i]['subList'][j]['city'] + "市")
                    # 对每个城市进行数据的赋值，写入csv
                    for key in keys2[2:]:
                        try:
                            if info[i]['subList'][j][key] == '':
                                info[i]['subList'][j][key] = '0'
                            each_city.append(info[i]['subList'][j][key])
                        except:
                            each_city.append('-1')
                    my2.writerow([c_id]+each_city)
                    c_id += 1

    def oversea_country_info(self,result):
        """
        :param result: 获取的总信息
        :return: 海外各国疫情情况
        'caseOutsideList':  [
                            {'confirmed': '43242302',
                            'died': '696867',
                            'crued': '32830025',
                            'area': '美国',
                            'curConfirm': '9715410',
                            'confirmedRelative': '207690',
                            'diedRelative': '2803',
                            'curedRelative': '172404',
                            'curConfirmRelative': '32483',
                            'relativeTime': '1632153600',
                            'icuDisable': '1',
                            'subList': [
                                        {   'city': '纽约州',
                                            'confirmed': '2458407',
                                            'died': '55552',
                                            'crued': '2120004',
                                            'curConfirm': '282851',
                                            'relativeTime': '1632153600',
                                            'curedPercent': '86.2%',
                                            'diedPercent': '2.3%'
                                        },
                                        ],
                            'curedPercent': '90.0%',
                            'diedPercent': '0.8%'
                            },
                            ],
        """

        info = result['component'][0]['caseOutsideList']
        keys = ['id','area','confirmed','confirmedRelative','crued','curConfirm','curConfirmRelative','curedPercent','curedRelative','died','diedPercent','diedRelative','icuDisable']
        with open(self.filename4,'w') as f:
            my = csv.writer(f)
            my.writerow(keys)
            for i in range(len(info)):
                each_country = [i+1,info[i]['area'],info[i]['confirmed'],info[i]['confirmedRelative'],info[i]['crued'],
                                info[i]['curConfirm'],info[i]['curConfirmRelative'],info[i]['curedPercent'],
                                info[i]['curedRelative'],info[i]['died'],info[i]['diedPercent'],info[i]['diedRelative'],
                                info[i]['icuDisable']]
                my.writerow(each_country)

    def continent_info(self,result):
        """
        'globalList': 存放6大洲,钻石公主号邮轮,最热门的10个国家的疫情情况 （dict形式存放在list）
        'area': '亚洲',
        'subList':
                    'confirmed': 累计确诊
                    'died': 累计死亡
                    'crued': 累计治愈
                    'curConfirm': 现有确诊
                    'confirmedRelative': 累计确诊增量
                    'relativeTime': 时间戳
                    'country': 国家
        'died': 累计死亡
        'crued': 累计治愈
        'confirmed': 累计确诊
        'curConfirm': 现有确诊
        'confirmedRelative': 累计确诊增量
        'curedPercent': 治愈率
        'diedPercent': 死亡率
        :param result: 获取的总信息
        :return: 六大洲疫情总结（除南极洲）
        """

        info = result['component'][0]['globalList']
        keys = ['id','area','confirmed','confirmedRelative','crued','curConfirm','curedPercent','died','diedPercent']
        with open(self.filename5,'w') as f:
            my = csv.writer(f)
            my.writerow(keys)
            for i in range(7):
                each_continent = [i+1,info[i]['area'],info[i]['confirmed'],info[i]['confirmedRelative'],
                                  info[i]['crued'],info[i]['curConfirm'],info[i]['curedPercent'],
                                  info[i]['died'],info[i]['diedPercent']]
                my.writerow(each_continent)

    def oversea_trend_info(self,result):
        """
        :param result: 获取的总信息
        :return: 海外疫情发展趋势
        'allForeignTrend': {'updateDate': ['2.15','...','9.21'],
                                        'list': [
                                                {'name': '累计确诊',
                                                'data': [626,...,229896604]},
                                                {'name': '治愈',
                                                'data': [86,...,206585667]},
                                                {'name': '死亡',
                                                'data': [2,...,4711210]},
                                                {'name': '现有确诊',
                                                'data': [538,...,18599727]},
                                                {'name': '新增确诊',
                                                'data': [21,...,534005]}
                                                ]
                                        },
        """

        info = result['component'][0]['allForeignTrend']
        oversea_tend = ['id','date','confirmed','cured','died','curConfirm','curConfirmRelative']
        y = str(datetime.datetime.now().year) + '.'
        with open(self.filename6, 'w') as f:
            my = csv.writer(f)
            my.writerow(oversea_tend)
            id = 1
            for i in range(len(info['updateDate'])-60,len(info['updateDate'])):
                date = y + info['updateDate'][i]
                date = datetime.datetime.strptime(date, '%Y.%m.%d').strftime("%Y-%m-%d")
                info_list = [id,date,
                             info['list'][0]['data'][i],
                             info['list'][1]['data'][i],
                             info['list'][2]['data'][i],
                             info['list'][3]['data'][i],
                             info['list'][4]['data'][i]]
                id += 1
                my.writerow(info_list)

    def summary(self,result):
        """
        :param result: 获取的总信息
        :return: 中国和海外疫情总结
        'summaryDataIn': {  'confirmed': '124244',
                            'died': '5690',
                            'cured': '115914',
                            'asymptomatic': '342',
                            'asymptomaticRelative': '9',
                            'unconfirmed': '4',
                            'relativeTime': '1632153600',
                            'confirmedRelative': '59',
                            'unconfirmedRelative': '2',
                            'curedRelative': '41',
                            'diedRelative': '1',
                            'icu': '14',
                            'icuRelative': '2',
                            'overseasInput': '8868',
                            'unOverseasInputCumulative': '115364',
                            'overseasInputRelative': '25',
                            'unOverseasInputNewAdd': '22',
                            'curConfirm': '2640',
                            'curConfirmRelative': '6',
                            'icuDisable': '1'
                        },
        summaryDataOut': {'confirmed': '230201801',
                           'died': '4717285',
                           'curConfirm': '18568653',
                           'cured': '206915863',
                           'confirmedRelative': '534005',
                           'curedRelative': '558575',
                           'diedRelative': '8568',
                           'curConfirmRelative': '-33138',
                           'relativeTime': '1632153600',
                           'curedPercent': '89.9%',
                           'diedPercent': '2.0%'
                           },
        """

        keys = ['id','area']
        china_values = [1,'china']
        oversea_values = [2,'oversea']
        info = result['component'][0]
        for key, value in info['summaryDataIn'].items():
            keys.append(key)
            china_values.append(value)
            if key in info['summaryDataOut'].keys():
                oversea_values.append(info['summaryDataOut'][key])
            else:
                oversea_values.append('None')
        with open(self.filename7, 'w') as f:
            my = csv.writer(f)
            my.writerow(keys)
            my.writerow(china_values)
            my.writerow(oversea_values)

    def deal_tend(self):
        today = datetime.datetime.today()
        yestoday = (today + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        today = today.strftime('%Y-%m-%d')
        pre_df = pd.read_csv('./疫情数据/{}/tend.csv'.format(yestoday), encoding='gbk')
        now_df = pd.read_csv('./疫情数据/{}/summary.csv'.format(yestoday), encoding='gbk')
        next_df = pre_df.drop(0)
        next_df['id'] = next_df['id'] - 1
        new_row = pd.DataFrame({
            'id': 45,
            'date': yestoday,
            'curConfirm': now_df.loc[0, 'curConfirm'],
            'confirmed': now_df.loc[0, 'confirmed'],
            'cured': now_df.loc[0, 'cured'],
            'died': now_df.loc[0, 'died'],
            'curConfirmRelative': now_df.loc[0, 'curConfirmRelative'],
            'overseasInputRelative': now_df.loc[0, 'overseasInputRelative']}, index=[1])
        next_df = next_df.append(new_row, ignore_index=True)
        next_df.to_csv('./疫情数据/{}/tend.csv'.format(today), index=False)
