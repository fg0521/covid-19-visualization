import pprint
import time
import pymysql

class Read_sql():

    def __init__(self):
        """
        初始化连接数据库
        """
        self.con = pymysql.connect(host='localhost', user='root', password='password', port=3306, database='fg')
        self.cur = self.con.cursor()

    def select_summary(self):
        """
        :return:累计确诊/累计死亡/累计治愈/现有确诊/境外输入
        """
        sql = 'select confirmed,died,cured,curConfirm,overseasInput,' \
              'confirmedRelative,diedRelative,curedRelative,curConfirmRelative,overseasInputRelative from summary'
        l = []
        try:
            self.cur.execute(sql)
            summary = self.cur.fetchone()
            for i in range(10):
                if i > 4 and int(summary[i]) >= 0:
                    l.append('+'+summary[i])
                else:
                    l.append(summary[i])
            return l
        except:
            return False
        finally:
            self.cur.close()

    def select_tend(self):
        """
        :return: 新增确诊/境外输入（表1）,累计确诊/累计治愈/累计死亡
        """
        sql = 'select date,curConfirmRelative,overseasInputRelative,confirmed,cured,died,curConfirm from china_tend'

        date = []
        curRel = []
        overseaRel = []
        confirmed = []
        cured = []
        died = []
        curC = []
        try:
            self.cur.execute(sql)
            tend = self.cur.fetchall()
            for each in tend:
                date.append(each[0])
                curRel.append(each[1])
                overseaRel.append(each[2])
                confirmed.append(each[3])
                cured.append(each[4])
                died.append(each[5])
                curC.append(each[6])
            return [date,curRel,overseaRel,confirmed,cured,died,curC]
        except:
            return False
        finally:
            self.cur.close()

    def select_province(self):
        """
        :return: 存在确诊新冠的地区
        """
        sql = 'select area,curConfirm,curConfirmRelative from province where curConfirm > 0'
        area = []
        curCon = []
        curConRel = []
        try:
            self.cur.execute(sql)
            prov = self.cur.fetchall()
            for each in prov:
                area.append(each[0])
                curCon.append(each[1])
                curConRel.append(each[2])

            return [area,curCon,curConRel]
        except:
            return False
        finally:
            self.cur.close()

    def select_map(self):
        """
        :return: 现有确诊和累计确诊
        """
        sql = 'select area,curConfirm,confirmed from province'
        curCon = []
        confirmed = []
        try:
            self.cur.execute(sql)
            map = self.cur.fetchall()
            for each in map:

                curCon.append([each[0],each[1]])
                confirmed.append([each[0],each[2]])
            return [curCon,confirmed]
        except:
            return False
        finally:
            self.cur.close()

    def select_city(self):
        """
        :return: 每个省份城市的新冠疫情
        """
        sql = 'select city,confirmed,curConfirm from cities'
        pro_names = ['西藏','青海','贵州','吉林','新疆','宁夏','内蒙古','甘肃','天津','山西','陕西','辽宁',
                      '黑龙江','海南','河北','云南','广西','福建','上海','北京','江苏','四川','山东','江西',
                     '重庆','安徽','湖南','河南','广东','浙江','湖北','香港','澳门','台湾']
        all_city ={}
        try:
            self.cur.execute(sql)
            cities = self.cur.fetchall()
            for province in pro_names:
                city = []
                confirmed = []
                curconfirm = []
                for each in cities:
                    if province == each[0][:each[0].find('_')]:
                        city.append(each[0][each[0].find('_')+1:])
                        confirmed.append(each[1])
                        curconfirm.append(each[2])
                all_city[province]=[city,confirmed,curconfirm]
            return all_city
        except:
            return False
        finally:
            self.cur.close()

    def select_hotwords(self):
        """
        :return: 新闻要点
        """
        sql = 'select id,date,content,link from hotwords order by id limit 0,20'
        try:
            self.cur.execute(sql)
            h_word = self.cur.fetchall()
            n_words = {}
            for word in h_word:
                if len(word[2]) >= 20:
                    n_words['word' + str(word[0])] = [str(word[1])+',' + word[2][:20]+'...',word[3][:-1]]
                else:
                    n_words['word' + str(word[0])] = [str(word[1]) + ',' + word[2], word[3][:-1]]
            return n_words
        except:
            return False

        finally:
            self.cur.close()

    def select_localhot(self):
        """
        :return: 当地热点
        """
        sql = 'select content,link from local_hot order by date desc limit 0,15'
        try:
            self.cur.execute(sql)
            h_word = self.cur.fetchall()
            l_words = {}
            cnt = 1
            for word in h_word:
                if len(word[0]) >= 24:
                    l_words['word' + str(cnt)] = [word[0][:24] + '...', word[1][:-1]]
                else:
                    l_words['word' + str(cnt)] = [word[0], word[1][:-1]]
                cnt+=1
            return l_words
        except:
            return False
        finally:
            self.cur.close()

    def select_wordcloud(self):
        """
        :return: 词云
        """
        sql = 'select id,content,count from wordcloud order by id'
        try:
            self.cur.execute(sql)
            wordcloud = self.cur.fetchall()
            wd = []
            for each in wordcloud[:150]:
                wd.append((each[1],each[2][:-1]))
            return wd

        except:
            return False
        finally:
            self.cur.close()

    def select_riskarea(self):
        """
        :return: 风险区域
        """
        sql = 'select id,type,address,lon,lat from risk_area order by id'
        try:
            self.cur.execute(sql)
            risk = self.cur.fetchall()
            high_data = []
            mid_data = []
            dec_data = []
            turn_down = []
            turn_up = []
            inc_data = []
            for each in risk:
                if each[1] == 'high_risk':
                    high_data.append((each[2], '高风险地区'))
                elif each[1] == 'mid_risk':
                    mid_data.append((each[2], '中风险地区'))
                elif each[1] == 'dec_mid_risk' or each[1] == 'pre_high_risk':
                    dec_data.append((each[2], '新减风险地区'))
                elif each[1] == 'down_mid_risk':
                    turn_down.append((each[2], '转变为中风险地区'))
                elif each[1] == 'up_high_risk':
                    turn_up.append((each[2], '转变为高风险地区'))
                elif each[1] == 'inc_mid_risk' or each[1] == 'new_high_risk':
                    inc_data.append((each[2], '新增风险地区'))
            return [high_data,mid_data,dec_data,inc_data,turn_down,turn_up]

        except:
            return False
        finally:
            self.cur.close()

    def select_points(self,c):
        """
        :param c: 城市名称
        :return: 疫情服务点
        """
        sql = 'select name,area,address,tel from serve_points where city="{}"'.format(c)
        try:
            self.cur.execute(sql)
            point = self.cur.fetchall()
            p = []
            for i in point:
                p.append([i[0], '所属:'+i[1] + '<br/>' +'地址:'+i[2]+ '<br/>' + '电话:'+i[3][:-1]])
            return p
        except:
            return False
        finally:
            self.cur.close()

# sql = Read_sql()
# p = sql.select_points('嘉兴市')
# print(p)