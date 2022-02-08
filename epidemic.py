# -*- coding:utf-8 -*-

import datetime
import json

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request,render_template, jsonify
from flask_apscheduler import APScheduler

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Geo, Map, WordCloud, Grid, Liquid, BMap
import time

from pyecharts.commons import utils

from pyecharts.globals import GeoType
from get_pos import Your_Pos
from read_from_mysql import Read_sql



class SchedulerConfig():
    """
    定时调用网络爬虫和查询时间
    job1:查询任务
    job2:爬虫任务
    """
    JOBS = [
        {
            'id': 'job1',  # 任务id
            'func': '__main__:select_info',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'interval',  # date:一次性指定固定时间，只执行一次     interval:间隔调度，隔多长时间执行一次     cron:指定相对时间执行，比如：每月1号、每星期一执行
            'hours':1.1,
        },
        {
            'id':'job2',
            'func':'spider:main',
            'args':None,
            'trigger':'interval',
            'hours': 1,
        }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

def select_info():
    """
    查询数据
    :return:
    """
    global line_data, bar_data, today, riskarea,bmap_data,\
        map_data, city, num, wc_data, national_hot, local_hot,city_name
    ip = Your_Pos()
    if ip.check_ip():
        city_name = ip.get_location()
    else:
        city_name='湖州市'
    # city_name = '湖州市'

    sql1 = Read_sql()
    line_data = sql1.select_tend()
    sql2 = Read_sql()
    bar_data = sql2.select_province()
    sql3 = Read_sql()
    map_data = sql3.select_map()
    sql4 = Read_sql()
    city = sql4.select_city()
    sql5 = Read_sql()
    num = sql5.select_summary()
    sql6 = Read_sql()
    wc_data = sql6.select_wordcloud()
    sql7 = Read_sql()
    national_hot = sql7.select_hotwords()
    sql8 = Read_sql()
    local_hot = sql8.select_localhot()
    sql9 = Read_sql()
    riskarea = sql9.select_riskarea()
    sql0 = Read_sql()
    bmap_data = sql0.select_points(city_name)
    print('==========数据查询完成==========')
    # createTimer()


global data,map_style
app = Flask(__name__)
app.config.from_object(SchedulerConfig())


@app.route("/", methods=['POST', 'GET'])
def index():
    """
    根路径，渲染模板index.html
    :return: 渲染完成的模板
    """
    global data
    if request.method == 'POST':
        # 'options'：为<select name="options">标签name的值
        data = request.form.get('city')
        with open('./static/other/selected.txt', 'w') as f:
            f.write(data)
    return render_template("grid.html")



def bar_base() -> Bar:

    global bar_data
    bar = (
        Bar(init_opts=opts.InitOpts(width="90%"))
            .add_xaxis(xaxis_data=bar_data[0])
            .add_yaxis(series_name="现有确诊",
                       y_axis=bar_data[1],
                       z=0,
                       itemstyle_opts = opts.ItemStyleOpts(color="#f94467"))
            .extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True,  # 显示轴线
                                                                             linestyle_opts=opts.LineStyleOpts(
                                                                                 color='#c1f0fe', )
                                                                             ),
                                             axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                             interval=20,
                                             )
                         )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="当前确诊区域",
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                                               font_weight='bold',
                                                                                               font_size=14),
                                                       subtitle="仅显示存在新冠的区域",
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#d5d5d5',
                                                                                                  font_size=8),
                                                       item_gap=-4,
                                                       pos_top="2%",
                                                       pos_left="4%"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_bottom="1%",
                                                         orient="horizontal",
                                                         inactive_color='#818181',
                                                         textstyle_opts=opts.TextStyleOpts(color='#fff'),
                                                         ),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                                      axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe")
                                                                                      ),
                                                      ),
                             xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe")
                                                                                      )
                                                      ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           orient='horizontal',
                                                           pos_top="3%",
                                                           pos_left="50%",
                                                           feature=opts.ToolBoxFeatureOpts(
                                                               save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                                   is_show=True,
                                                                   type_="png",
                                                                   background_color="#0b122f",
                                                                   pixel_ratio=5),
                                                               restore=opts.ToolBoxFeatureRestoreOpts(is_show=True,
                                                                                                      ),
                                                               data_view=opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                                                         is_read_only=True,
                                                                                                         ),
                                                               data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                                               magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=True,
                                                                                                           type_=[
                                                                                                               'line',
                                                                                                               'bar'],
                                                                                                           ),
                                                               brush=opts.ToolBoxFeatureBrushOpts(type_="clear")
                                                               )
                                                           ),
                             )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=bar_data[0])
            .add_yaxis(series_name="新增确诊增量",
                       y_axis=bar_data[2],
                       yaxis_index=1,
                       is_symbol_show=False,
                       is_smooth=True,
                       itemstyle_opts=opts.ItemStyleOpts(color="#93eeff"),
                       linestyle_opts=opts.LineStyleOpts(width=2) )

    )

    all = bar.overlap(line)
    grid1 = Grid().add(all, grid_opts=opts.GridOpts(pos_left="12%"), is_control_axis_index=True)
    return grid1
@app.route("/barChart")
def get_bar_chart():
    """
    :return: 现有确诊和确诊区域分布
    """
    c = bar_base()
    return c.dump_options_with_quotes()


def line_base() -> Line:

    global line_data
    line = (
        Line()
            .add_xaxis(xaxis_data=line_data[0])

            .add_yaxis(series_name="累计确诊",
                       y_axis=line_data[3],
                       label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False,
                       is_smooth=True,
                       color='#4673bc',
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )
            .add_yaxis(series_name="累计治愈",
                       y_axis=line_data[4],
                       label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False,
                       is_smooth=True,
                       color='#e94141',
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )
            .add_yaxis(series_name="累计死亡",
                       y_axis=line_data[5],
                       label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False,
                       is_smooth=True,
                       color='#00b65e',
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )
            .add_yaxis(series_name="现有确诊",
                       y_axis=line_data[6],
                       label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False,
                       is_smooth=True,
                       color='#e4c02e',
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )


            .set_global_opts(title_opts=opts.TitleOpts(title="累计确诊-死亡-治愈趋势",
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                                               font_weight='bold',
                                                                                               font_size=14),
                                                       subtitle="近45天变化趋势",
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#d5d5d5',
                                                                                                  font_size=8),
                                                       item_gap=-4,
                                                       pos_top="2%",
                                                       pos_left="4%"),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),
                             yaxis_opts=opts.AxisOpts(type_="value",

                                                      axistick_opts=opts.AxisTickOpts(is_show=True,
                                                                                      ),
                                                      axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe")
                                                                                      ),

                                                      ),
                             xaxis_opts=opts.AxisOpts(type_="category",
                                                      
                                                      axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe",
                                                                                          )
                                                                                      ),
                                                      axispointer_opts=opts.AxisPointerOpts(is_show=True, ),
                                                      ),

                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_bottom="1%",
                                                         orient="horizontal",
                                                         inactive_color='#818181',
                                                         textstyle_opts=opts.TextStyleOpts(color='#fff'),
                                                         ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           orient='horizontal',
                                                           pos_top="3%",
                                                           pos_left="50%",
                                                           
                                                           feature=opts.ToolBoxFeatureOpts(
                                                                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                                   is_show=True,
                                                                   type_="png",
                                                                   background_color="#0b122f",
                                                                   pixel_ratio=5),
                                                               restore=opts.ToolBoxFeatureRestoreOpts(is_show=True,
                                                                                                      ),
                                                               data_view=opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                                                         is_read_only=True,
                                                                                                         ),
                                                               data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                                               magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=True,
                                                                                                           type_=[
                                                                                                               'line',
                                                                                                               'bar'],
                                                                                                           ),
                                                               brush=opts.ToolBoxFeatureBrushOpts(type_="clear")
                                                           )
                                                           ),
                             )

    )
    grid2 = Grid().add(line, grid_opts=opts.GridOpts(pos_left="70"))
    return grid2
@app.route("/lineChart")
def get_line_chart():
    """
    :return:累计治愈、死亡、确诊、现有
    """
    l = line_base()
    return l.dump_options_with_quotes()


def line2_base() -> Line:

    global line_data
    line = (
        Line()
            .add_xaxis(xaxis_data=line_data[0])
            .add_yaxis(series_name="国内新增趋势",
                       is_smooth=True,
                       symbol="emptyCircle",
                       is_symbol_show=False,
                       color="#ff444e",
                       y_axis=line_data[1],
                       label_opts=opts.LabelOpts(is_show=False),
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )
            .add_yaxis(series_name="海外输入新增趋势",
                       is_smooth=True,
                       symbol="emptyCircle",
                       is_symbol_show=False,
                       color="#37f9ff",
                       y_axis=line_data[2],
                       label_opts=opts.LabelOpts(is_show=False),
                       linestyle_opts=opts.LineStyleOpts(width=2),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="国内新增-国外输入趋势",
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                                               font_weight='bold',
                                                                                               font_size=14),
                                                       subtitle="近45天变化趋势",
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#d5d5d5',
                                                                                                  font_size=8),
                                                       item_gap=-4,
                                                       pos_top="2%",
                                                       pos_left="4%"),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_bottom="1%",
                                                         orient="horizontal",
                                                         inactive_color='#818181',
                                                         textstyle_opts=opts.TextStyleOpts(color='#fff'), ),
                             tooltip_opts=opts.TooltipOpts(trigger="none"),
                             xaxis_opts=opts.AxisOpts(type_="category",

                                                      axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe")
                                                                                      ),
                                                      axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                                                            ),

                                                      ),
                             yaxis_opts=opts.AxisOpts(type_="value",
                                                      splitline_opts=opts.SplitLineOpts(is_show=False,
                                                                                        # linestyle_opts=opts.LineStyleOpts(opacity=1)
                                                                                        ),
                                                      axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                                                      linestyle_opts=opts.LineStyleOpts(
                                                                                          color="#c1f0fe")
                                                                                      ),
                                                      ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           orient='horizontal',
                                                           pos_top="3%",
                                                           pos_left="50%",
                                                           feature=opts.ToolBoxFeatureOpts(
                                                               save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                                   is_show=True,
                                                                   type_="png",
                                                                   background_color="#0b122f",
                                                                   pixel_ratio=5),
                                                               restore=opts.ToolBoxFeatureRestoreOpts(is_show=True,
                                                                                                      ),
                                                               data_view=opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                                                         is_read_only=True,
                                                                                                         ),
                                                               data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                                               magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=True,
                                                                                                           type_=[
                                                                                                               'line',
                                                                                                               'bar'],
                                                                                                           ),
                                                               brush=opts.ToolBoxFeatureBrushOpts(type_="clear")
                                                           )
                                                           ),
                             )
    )

    return line
@app.route("/line2Chart")
def get_Line2_chart():
    """
    :return:国内新增和海外输入
    """
    l = line2_base()
    return l.dump_options_with_quotes()


def geo_base() -> Geo:
    global riskarea
    today = datetime.date.today()
    geo = (
        Geo()
            .add_schema(maptype="china",
                        layout_center=["50%", "55%"],
                        layout_size='110%',
                        itemstyle_opts=opts.ItemStyleOpts(color="#1c2d52",
                                                          border_color="#07cdee",
                                                          border_width=1,
                                                          opacity=0.7,
                                                          ),
                        )
            .add_coordinate_json('./疫情数据/{}/hra.json'.format(today))
            .add(
            "高风险地区",
            data_pair=riskarea[0],
            symbol_size=45,
            color='rgba(255, 240, 0,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .add_coordinate_json('./疫情数据/{}/mra.json'.format(today))
            .add(
            "中风险地区",
            data_pair=riskarea[1],
            symbol_size=25,
            color='rgba(0, 255, 0,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .add_coordinate_json('./疫情数据/{}/dec.json'.format(today))
            .add(
            "新减风险地区",
            data_pair=riskarea[2],
            symbol_size=15,
            color='rgba(255, 45, 173,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .add_coordinate_json('./疫情数据/{}/inc.json'.format(today))
            .add(
            "新增风险地区",
            data_pair=riskarea[3],
            symbol_size=25,
            color='rgba(13, 207, 225,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .add_coordinate_json('./疫情数据/{}/down.json'.format(today))
            .add(
            "转变为中风险地区",
            data_pair=riskarea[4],
            symbol_size=25,
            color='rgba(255, 117, 25,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .add_coordinate_json('./疫情数据/{}/up.json'.format(today))
            .add(
            "转变为高风险地区",
            data_pair=riskarea[5],
            symbol_size=45,
            color='rgba(228, 28, 74,0.8)',
            type_=GeoType.EFFECT_SCATTER,
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="当前全国风险区域分布({}+{})".format(len(riskarea[0]), len(riskarea[1])),
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                                               font_size=24,),
                                                       pos_top="1%",
                                                       pos_left="4%"),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_left='center',

                                                         # pos_right="60%",
                                                         pos_top="8%",
                                                         orient='horizontal',
                                                         item_width=30,
                                                         item_height=20,
                                                         inactive_color='#fff',
                                                         textstyle_opts=opts.TextStyleOpts(color="#fff",font_weight='bold'),
                                                         ),
                             )

    )
    return geo
@app.route("/geoChart")
def get_geo_chart():
    """
    :return: 高风险地区分布
    """
    g = geo_base()
    return g.dump_options()


def map_base() -> Map:
    pieces = [{"max": 999999, "min": 10001, "label": ">10000", "color": "#c20044"},
              {"max": 9999, "min": 1000, "label": "1000-9999", "color": "#e9103f"},
              {"max": 999, "min": 100, "label": "100-999", "color": "#ec6575"},
              {"max": 99, "min": 10, "label": "10-99", "color": "#206dbe"},
              {"max": 9, "min": 1, "label": "1-9", "color": "#164693"},
              {"max": 0, "min": 0, "label": "0", "color": "#172a5d"},
              ]

    global map_data
    map = (
        Map()
            .add(series_name="现有确诊人数",
                 data_pair=map_data[0],
                 maptype="china",
                 is_selected=True,
                 is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False),
                 layout_center=["50%", "55%"],
                 layout_size='110%',
                 itemstyle_opts=opts.ItemStyleOpts(border_color='#332ddf0')
                 )
            .add(series_name="累计确诊人数",
                 data_pair=map_data[1],
                 maptype="china",
                 is_selected=False,
                 is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False),
                 layout_center=["50%", "55%"],
                 layout_size='110%',
                 itemstyle_opts=opts.ItemStyleOpts(border_color='#332ddf0')
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="全国疫情分布",
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',font_size=24),
                                                       pos_top="1%",
                                                       pos_left="4%"),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         selected_mode="single",
                                                         pos_top="8%",
                                                         item_width=30,
                                                         item_height=20,
                                                         pos_left='center',

                                                         inactive_color='#fff',
                                                         textstyle_opts=opts.TextStyleOpts(color="#fff")),
                             visualmap_opts=opts.VisualMapOpts(is_show=True,
                                                               is_piecewise=True,
                                                               pieces=pieces,
                                                               orient="vertical",
                                                               pos_left="4%",
                                                               pos_bottom="4%",
                                                               item_width=30,
                                                               item_height=20,
                                                               textstyle_opts=opts.TextStyleOpts(color='#fff'),
                                                               ),

                             )
    )
    return map
@app.route("/mapChart")
def get_map_chart():
    """
    :return: 现有/累计确诊分布
    """
    m = map_base()
    return m.dump_options_with_quotes()


def map2_base() -> Map:
    global data,city
    pieces = [
        {"max": 999999, "min": 1000, "label": ">1000", "color": "#c20044"},
        {"max": 999, "min": 100, "label": "100-999", "color": "#e9103f"},
        {"max": 99, "min": 1, "label": "1-99", "color": "#ec6575"},
        {"max": 0, "min": 0, "label": "0", "color": "#164693"},
        {"max": '-1', "min": '-1', "label": "-1", "color": "#adadad"},
    ]
    info = city[data]
    map2 = (
        # 设置地图大小
        Map()
            .add(series_name="现有确诊",
                 data_pair=[list(z) for z in zip(info[0], info[2])],
                 maptype=data,
                 is_selected=True,
                 is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False),
                 layout_center=["60%", "55%"],
                 layout_size='75%',
                 itemstyle_opts=opts.ItemStyleOpts(border_color='#332ddf0')
                 )
            .add(series_name="累计确诊",
                 data_pair=[list(z) for z in zip(info[0], info[1])],
                 maptype=data,
                 is_selected=False,
                 is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False),
                 layout_center=["60%", "55%"],
                 layout_size='75%',
                 itemstyle_opts=opts.ItemStyleOpts(border_color='#332ddf0')
                 )

            # 设置全局变量  is_piecewise设置数据是否连续，split_number设置为分段数，pices可自定义数据分段
            # is_show设置是否显示图例
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=True,
                                                         selected_mode="single",
                                                         # pos_left='50%',
                                                         # pos_bottom='5%',
                                                         item_width=25,
                                                         item_height=16,
                                                         orient='horizontal',
                                                         pos_left='34%',
                                                         pos_top="3%",
                                                         inactive_color='#fff',
                                                         textstyle_opts=opts.TextStyleOpts(color="#fff")),
                             title_opts=opts.TitleOpts(title="%s疫情分布" % (data),
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',font_size=14),
                                                       subtitle="香港/澳门/台湾暂无准确数据",
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#d5d5d5',font_size=8),
                                                       pos_left='4%',
                                                       item_gap=-4,
                                                       pos_top="2%",),
                             visualmap_opts=opts.VisualMapOpts(is_show=True,
                                                               is_piecewise=True,
                                                               pieces=pieces,
                                                               pos_left='4%',
                                                               pos_top="20%",
                                                               # pos_bottom="20%",
                                                               textstyle_opts=opts.TextStyleOpts(color='#fff'),

                                                               item_width=25,
                                                               item_height=16,
                                                               )
                             )
    )
    return map2
@app.route("/map2Chart")
def get_map2_chart():
    """
    :return: 各省份城市现有/累计确诊分布
    """
    m = map2_base()
    return m.dump_options_with_quotes()


def bmap_base() -> BMap:
    global bmap_data,map_style
    #在Flask的app.py里生成chart的时候，用utils.JsCode(tooltips)包装formatter，
    #这样dump_options()出来的是含有str:function形式的“疑似”json字串，
    #然后直接返回这个字串，注意这里不要做任何json转换，因为带有str:function形式的根本就不是json
    jscode = """function (params){
        return params.value[2];
        }
        """
    bmap = (
        BMap()

            .add_schema(baidu_ak="wjb0GWDI3ZqXu0L9MBbfviRR8DTv0il9",
                        center=[120.128467, 30.878793],
                        zoom=12,
                        is_roam=True,
                        map_style={"styleJson": map_style},

                        )
            .add(type_="effectScatter",
                 series_name="附近疫情服务点",
                 data_pair=bmap_data,
                 label_opts=opts.LabelOpts(formatter="{b}"),
                 symbol_size=15,
                 itemstyle_opts=opts.ItemStyleOpts(color="#00F59F"),
                 effect_opts=opts.EffectOpts(),
                 tooltip_opts=opts.TooltipOpts(formatter=utils.JsCode(jscode)),#utils.JsCode("""function (params) {        return params.name + ' : ' + params.value[2];    },""")


                 )

            .set_global_opts(legend_opts=opts.LegendOpts(inactive_color='#fff',
                                                         textstyle_opts=opts.TextStyleOpts(color="#fffd68",
                                                                                           font_weight='bold',
                                                                                           ),
                                                         )
                             )
    )
    return bmap
@app.route("/bmapChart")
def get_bmap_chart():
    """
    :return: 百度地图疫情服务点分布
    """
    bmap = bmap_base()
    return bmap.dump_options()


def liquid_base() -> Liquid:
    global num
    dead_rate = round(int(num[1]) / int(num[0]), 4)
    cure_rate = round(int(num[2]) / int(num[0]), 4)
    conf_rate = round(int(num[3]) / int(num[0]), 4)
    input_rate = round(int(num[4]) / int(num[0]), 4)

    l1 = (
        Liquid()
            .add(series_name="死亡率",
                 data=[dead_rate],
                 center=["15%", "60%"],
                 outline_border_distance=4,
                 label_opts=opts.LabelOpts(font_size=10,
                                           position="inside",
                                           formatter=f"死亡率\n{round(dead_rate * 100, 2)}%", ))
            .set_global_opts(title_opts=opts.TitleOpts(title="新冠治愈率-死亡率",
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                                               font_weight='bold',
                                                                                               font_size=14),

                                                       pos_top="2%",
                                                       pos_left="4%",

                                                       ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           orient='horizontal',
                                                           pos_top="3%",
                                                           pos_left="50%",
                                                           feature=opts.ToolBoxFeatureOpts(
                                                               save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                                   is_show=True,
                                                                   type_="png",
                                                                   background_color="#0b122f",
                                                                   pixel_ratio=5),
                                                               restore=opts.ToolBoxFeatureRestoreOpts(is_show=True,
                                                                                                      ),
                                                               data_view=opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                                                         is_read_only=True,
                                                                                                         ),
                                                               data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                                               magic_type=opts.ToolBoxFeatureMagicTypeOpts(
                                                                   is_show=False, ),
                                                               brush=opts.ToolBoxFeatureBrushOpts(type_="clear")
                                                           )
                                                           ),
                             )
    )

    l2 = Liquid().add(
        series_name="治愈率",
        data=[cure_rate],
        center=["38%", "60%"],
        outline_border_distance=4,
        label_opts=opts.LabelOpts(
            font_size=10,
            formatter=f"治愈率\n{round(cure_rate * 100, 2)}%",
            position="inside",
        ),
    )

    l3 = Liquid().add(
        series_name="现有率",
        data=[conf_rate],
        center=["61%", "60%"],
        outline_border_distance=4,
        label_opts=opts.LabelOpts(
            font_size=10,
            formatter=f"现有率\n{round(conf_rate * 100, 2)}%",
            position="inside",
        ),
    )

    l4 = Liquid().add(
        series_name="输入率",
        data=[input_rate],
        center=["84%", "60%"],
        outline_border_distance=4,
        label_opts=opts.LabelOpts(
            font_size=10,
            formatter=f"输入率\n{round(input_rate * 100, 2)}%",
            position="inside",
        ),
    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts()).add(l3,
                                                                                            grid_opts=opts.GridOpts()).add(
        l4, grid_opts=opts.GridOpts())

    return grid
@app.route("/liquidChart")
def get_liquid_chart():
    """
    :return: 死亡率、治愈率、现有率、境外输入率
    """
    l = liquid_base()
    return l.dump_options_with_quotes()


def wordcloud_base() -> WordCloud:
    global wc_data
    cloud = (
        WordCloud()
            .add(series_name='高风险地区',
                 data_pair=wc_data,
                 word_size_range=[10, 40],
                 width="90%",
                 height="70%",
                 pos_top="20%",

                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="今日热词",
                                      title_textstyle_opts=opts.TextStyleOpts(color='#fff',
                                                                              font_weight='bold',
                                                                              font_size=14),
                                      pos_top="2%",
                                      pos_left="4%"
                                      ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          orient='horizontal',
                                          pos_top="3%",
                                          pos_left="50%",
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True,
                                                                                               type_="png",
                                                                                               background_color="#0b122f",
                                                                                               pixel_ratio=5),
                                              restore=opts.ToolBoxFeatureRestoreOpts(is_show=True,
                                                                                     ),
                                              data_view=opts.ToolBoxFeatureDataViewOpts(is_show=True,
                                                                                        is_read_only=True,
                                                                                        ),
                                              data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                              magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False,
                                                                                          ),
                                              brush=opts.ToolBoxFeatureBrushOpts(type_="clear")
                                          )
                                          ),

        )

    )
    return cloud
@app.route("/wordcloudChart")
def get_wordcloud_chart():
    """
    :return: 微博词云图
    """
    w = wordcloud_base()
    return w.dump_options_with_quotes()


@app.route("/time")
def get_time():
    """
    :return: 时间
    """
    cur_time = time.strftime("%Y{}%m{}%d{} %X").format("年", "月", "日")
    return "&nbsp;&nbsp;@截止至: " + cur_time


@app.route("/keynum")
def get_keynum():
    """
    :return: 关键大数字
    """
    global num
    return jsonify({'confirmed': num[0], 'died': num[1], 'cured': num[2], 'curConfirm': num[3], 'overseasInput': num[4],
                    'confirmedRelative': '较昨日' + num[5], 'diedRelative': '较昨日' + num[6],
                    'curedRelative': '较昨日' + num[7],
                    'curConfirmRelative': '较昨日' + num[8], 'overseasInputRelative': '较昨日' + num[9]})


@app.route('/hotwords')
def get_hotwords():
    """
    :return: 轮播图1
    """
    global national_hot
    return jsonify(national_hot)


@app.route('/local_hot')
def get_localhot():
    """
    :return: 轮播图2
    """
    global local_hot
    return jsonify(local_hot)


if __name__ == '__main__':
    with open('./static/other/selected.txt', 'r') as f:
        data = f.read()
        f.close()
    with open('./static/other/style.json') as file:
        map_style = json.load(file)
        file.close()
    # 为实例化的flask引入定时任务配置
    scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))
    scheduler.init_app(app)  # 把任务列表载入实例flask
    scheduler.start()  # 启动任务计划
    select_info()
    app.run()  # 设置debug=True是为了让代码修改实时生效，而不用每次重启加载
