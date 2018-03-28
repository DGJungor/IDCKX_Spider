import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='idckx', charset='utf8')

# 创建游标
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor = conn.cursor()

# 执行SQL，并返回收影响行数
cursor.execute("select * from idckx_spider_post")
effect_row = cursor.fetchall()

print(effect_row)
