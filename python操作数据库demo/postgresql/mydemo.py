#coding=utf-8
import pgdb
conn = pgdb.connect(user='chnesb', password='', host='127.0.0.1:3336', database='mydb')
#conn = pgdb.connect(user='liupeng', password='', host='192.168.8.128:5432', database='mydb')
#print dir(conn)
ssql = 'select version()'
cur = conn.cursor()

isql = """ INSERT INTO "public"."mytest" ("myid", "myname", "mydate", "myfee") VALUES ('1', 'liupengc_刘朋', '2016-10-31', '183.05'); """
isql = """ INSERT INTO mytest VALUES (%s,%s,%s,%s) """
ivalues = [['2','liupengc_刘朋', '2016-09-30', '183.05'],]
cur.executemany(isql, ivalues)
#rows = cur.fetchall()
#print r
#for r in rows:
#    print r[0]
    
cur.close()
conn.commit()
conn.close()



"""
/*
* 函数介绍: 输入一个文件类型的
* 输入参数: fn:文件的名称
* 输出参数: 可以迭代的gz的文件句柄
* 返回值:   可以迭代的gz的文件句柄
*/
"""
def demo():
    pass
###################################################################

"""
/*
* 函数介绍: 获得数据库的连接
* 输入参数: dbinfo_dict
            {
                "ip":"10.255.254.235",
                "port":3336,
                "dbuser":"chnesb",
                "dbpwd":"",
                "dbname":"mydb",
                "dbtype":"pg"
            }
            pg: postgresql 
            
* 输出参数: conn 
* 返回值:   conn
*/
"""
def get_conn(dbinfo_dict):
    if "PG" in dbinfo_dict['dbtype'].upper():
        user = dbinfo_dict['dbuser']
        password = dbinfo_dict['dbpwd']
        host = '%s:%s' % (dbinfo_dict['ip'],dbinfo_dict['port'])
        database = dbinfo_dict['database']
        return pgdb.connect(user=user, password=password, host=host, database=database)
    else:
        return None
###################################################################


"""
/*
* 函数介绍: 
* 输入参数: 
* 输出参数: 
* 返回值:   
*/
"""
def run_sql(dbinfo_dict,sqlstr):
    retcode = 0
    retmsg = ""
    conn = None
    cur  = None
    try:
        conn = get_conn(dbinfo_dict)
        cur = conn.cursor()
        cur.execute(sqlstr)
        conn.commit()
    except Exception,x:
        print x,type(x)
        if "already exists" in str(x).lower():
            retcode = 0
        elif "not exist" in str(x).lower():
            retcode = 0
        else:
            retcode = 1
        retmsg = str(x).strip()
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return retcode, retmsg
        
###################################################################


dbinfo_dict = {}
dbinfo_dict['dbuser'] = 'chnesb'
dbinfo_dict['dbpwd'] = ''
dbinfo_dict['ip'] = '10.255.254.235'
dbinfo_dict['port'] = '3336'
dbinfo_dict['database'] = 'mydb' 
dbinfo_dict['dbtype'] = 'PG' 

isql = 'drop table test'

print run_sql(dbinfo_dict,isql)




# https://my.oschina.net/aven92/blog/518928
# pip -i http://pypi.doubanio.com/simple/ install Sphinx
# index-url = http://pypi.doubanio.com/simple/