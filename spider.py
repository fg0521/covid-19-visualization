import datetime
import os
import time
from multiprocessing import Pool
from get_data import Get_data
from get_pos import Your_Pos
from get_risk_area import Risk_Area
from get_local_hw import Local_Info
from get_wordcloud import Wordcloud_Info
from save_to_mysql import Write_sql
from get_national_hw import National_Info



def main():
    today = datetime.date.today()

    ip = Your_Pos()
    if ip.check_ip():
        city = ip.get_location()
    else:
        city = '湖州市'

    path = './疫情数据/{}'.format(today)
    if not os.path.exists(path):
        os.makedirs(path)

    time_start = time.time()
    gd = Get_data(path)
    result = gd.parse_data()
    gd.china_trend_info(result)
    gd.province_info(result)
    gd.oversea_country_info(result)
    gd.continent_info(result)
    gd.oversea_trend_info(result)
    gd.summary(result)
    gd.deal_tend()
    time_gd = time.time()
    print("疫情数据获取完成,耗时{}s".format(time_gd-time_start))

    ra = Risk_Area(path)
    urls = ra.get_area()
    ra.call_coroutine(urls)
    ra.save_json()
    ra.comp()
    time_ra = time.time()
    print("高风险区域数据获取完成,耗时{}s".format(time_ra-time_gd))

    nation = National_Info(path)
    nation.get_nation()
    time_na = time.time()
    print("全国热点数据获取完成,耗时{}s".format(time_na-time_ra))


    local = Local_Info(path,city)
    local.call_coroutine()  # 调用方
    local.multi_process()
    time_lo = time.time()
    print("当地热搜数据获取完成,耗时{}s".format(time_lo-time_na))

    wcloud = Wordcloud_Info(path)
    wcloud.call_coroutine()
    wcloud.multi_process()
    wcloud.divide()
    time_wc = time.time()
    print("词云数据获取完成,耗时{}s".format(time_wc-time_lo))

    time_end = time.time()
    time_c = time_end - time_start
    mysql = Write_sql()
    mysql.write()

    print('一共耗时{}s'.format(time_c))

main()