# encoding: utf-8
"""
@author: zhaozilong
@contact: whuzhaozilong@whu.edu.cn
@time: 2023/1/5 15:38
"""
import pymysql


def get_mysql_link():
    """
    连接数据库
    guest:数据库名称
    return:db
    """
    try:
        db = pymysql.connect(host='127.0.0.1',
                             user='username',
                             passwd='password',
                             db='databasename',
                             charset='utf8')
        return db
    except ConnectionError as e:
        print("数据库连接异常!" + str(e))


class MysqlTool:
    def __init__(self):
        self.db = get_mysql_link()
        self.cursor = self.db.cursor()
        self.sql = "INSERT IGNORE INTO players (id, name, club, nation, league, first_position) " \
                   "VALUES (%s, %s, %s, %s, %s, %s);"

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def insert_datas(self, data):
        self.cursor.executemany(self.sql, data)
        self.db.commit()

    def insert_data(self, data):
        self.cursor.execute(self.sql, data)
        self.db.commit()


if __name__ == '__main__':
    mysql_tool = MysqlTool()
    listdata = [(48429, "Robert Lewandowski", "FC Barcelona", "Poland", "LaLiga Santander", "ST"),
                (48, "Robert", "FC-Bna", "land", "LaLr", "ST")]
    mysql_tool.insert_datas(listdata)
