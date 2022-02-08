# 导入pymysql方法
import pymysql
import datetime
class Write_sql():

    def __init__(self):
        """
        初始化连接数据库
        """
        config = {'host': 'localhost',
                  'port': 3306,
                  'user': 'root',
                  'passwd': 'password',
                  'charset': 'utf8mb4',
                  'local_infile': 1
                  }
        self.connect = pymysql.connect(**config)     # 包裹方式传参元组(*) 字典(**)
        self.cur = self.connect.cursor()



    def load_csv(self,csv_file_path, table_name, database='fg'):
        """
        :param csv_file_path: csv文件路径
        :param table_name: 表名称
        :param database: 数据库名称
        :return: 导入csv文件
        """
        file = open(csv_file_path, 'r', encoding='utf-8')   # 打开csv文件
        # 读取csv文件第一行字段名，创建表
        reader = file.readline()
        keys = reader.split(',')
        keys[-1] = keys[-1][:-1]
        # 创建建表语句
        colum = ''
        for key in keys:
            if key == 'id':
                colum = colum + '`' + key + '`' + ' int primary key,'
            elif key == 'date':
                colum = colum + '`' + key + '`' + ' date,'
            else:
                colum = colum + '`' + key + '`' + ' varchar(255),'
        colum = colum[:-1]
        # 编写sql，create_sql负责创建表，data_sql负责导入数据
        delete_sql = 'drop table if exists ' + table_name
        create_sql = 'create table if not exists ' + '`' + table_name + '`' + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8;'
        data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES" % (
        csv_file_path, table_name)
        self.cur.execute('use %s' % database)       # 使用数据库
        self.cur.execute('SET NAMES utf8;')         # 设置编码格式
        self.cur.execute('SET character_set_connection=utf8;')
        self.cur.execute(delete_sql)    # 执行delete_sql，删除表
        self.cur.execute(create_sql)    # 执行create_sql，创建表
        self.cur.execute(data_sql)      # 执行data_sql，导入数据
        self.connect.commit()

    def write(self):
        """
        :return: 写入数据库
        """
        today = datetime.date.today()
        path = '/Users/maoyufeng/Desktop/疫情分析/疫情数据/{}'.format(today)
        self.load_csv(path + "/summary.csv", "summary")
        # self.load_csv(path + "/china_tend.csv", "china_tend")
        self.load_csv(path + "/tend.csv", "china_tend")
        # self.load_csv(path + "/continent.csv", "continent")
        # self.load_csv(path + "/oversea_country.csv", "oversea_country")
        self.load_csv(path + "/province.csv", "province")
        self.load_csv(path + "/cities.csv", "cities")
        self.load_csv(path + "/nation_hw.csv", "hotwords")
        self.load_csv(path + "/local_hw.csv", "local_hot")
        self.load_csv(path + "/div_wordcloud.csv", "wordcloud")
        # self.load_csv(path + "/risk_areas.csv", "risk_area")
        self.load_csv(path + "/change.csv", "risk_area")
        self.load_csv("./static/other/serve_points.csv", "serve_points")


        # 关闭连接
        self.connect.close()
        self.cur.close()

