#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
cursor.execute("select * from tb7")

# 获取剩余结果的第一行数据
row_1 = cursor.fetchone()
# print row_1
# 获取剩余结果前n行数据
# row_2 = cursor.fetchmany(3)

# 获取剩余结果所有数据
# row_3 = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()
