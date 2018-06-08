#coding=utf-8
import sys
import os
import MySQLdb
import traceback
import datetime
import time


def get_create_table_sql(tabname, )





def format_exc(limit=None):
    """Like print_exc() but return a string. Backport for Python 2.3."""
    retmsg = ""
    try:
        etype, value, tb = sys.exc_info()
        retmsg = ''.join(traceback.format_exception(etype, value, tb, limit))
    finally:
        etype = value = tb = None
    return retmsg
    
'''
连接数据库:
inpara:
    conn_dict={}
    conn_dict['host'] = '192.168.0.11'
    conn_dict['user'] = 'root'
    conn_dict['passwd'] = 'liupeng'
    conn_port['port'] = 3306
    conn_port['db'] = 'test'
    conn_port['charset'] = 'utf8'
outpara1: 0:ok 1:err
outpara2: if outpara1 == ok conn_object ; else errmsg
'''
def get_conn(conn_dict):
    retcode = 0
    retmsg = ''
    
    
    try:
        conn = MySQLdb.connect(**conn_dict)
        #print dir(MySQLdb)
        #print dir(conn)
        retmsg = conn
    except Exception,x:
        retcode = 1
        retmsg = '%s:%s' % (str(x),format_exc())
    return retcode,retmsg
    

    
def test():
    conn_dict={}
    conn_dict['host'] = '192.168.0.11'
    conn_dict['user'] = 'root'
    conn_dict['passwd'] = 'liupeng'
    conn_dict['port'] = 3306
    conn_dict['db'] = 'test'
    conn_dict['charset'] = 'utf8'
    retcode , retmsg = get_conn(conn_dict)
    conn = None
    if 0 == retcode:
        conn = retmsg
    else:
        return
    try:
        #conn.close()
        cur = conn.cursor()
        mysql = 'SELECT 1'
        cur.execute(mysql)
        rows = cur.fetchall()
        print ">>>>>>>>>>>>",rows,rows[0][0] == 1
        cur.close()
        
        
        try:
            print "conn.ping:", conn.ping()
            help(conn.ping)
        except:
            pass
        mysql = 'DROP TABLE IF EXISTS `my_demo`;'
        cur = conn.cursor()
        cur.execute(mysql)
        mysql = """CREATE TABLE `my_demo` (
                      `my_int` int(255) DEFAULT NULL,
                      `my_str` varchar(255) DEFAULT NULL,
                      `my_time` datetime DEFAULT NULL,
                      `my_cmd` varchar(1024) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """
        cur.execute(mysql)
        cur.close()
        
        t1 = time.time()
        cur = conn.cursor()
        mysql = """ INSERT INTO my_demo VALUES (%s,%s,%s,%s) """
        sqlparams = []
        rowcounts = 100
        for i in xrange(rowcounts):
            row = (i,'%04d'%i, '2016-04-06 23:40:54', 'a=1,b=2,c=3,d=4')
            sqlparams.append(row)
        cur.executemany(mysql,sqlparams)
        print '>>>>',cur.rowcount
        cur.close()
        conn.commit()
        t2 = time.time()
        print 'insert [%d] costs: %.2f seconds' % (rowcounts,t2-t1,)
        mysql = """ select count(1) from my_demo """
        cur = conn.cursor()
        cur.execute(mysql)
        rows = cur.fetchall()
        for r in rows:
            print r
        cur.close()
        
        t1 = time.time()
        mysql = """ update  my_demo set my_int = 11111 where  my_int=99999"""
        t1 = time.time()
        cur = conn.cursor()
        cur.execute(mysql)
        print 'update>>>>>>>:',cur.rowcount
        conn.commit()
        cur.close()
        t2 = time.time()
        print 'update [%d] costs: %.2f seconds' % (rowcounts,t2-t1,)
        
    except Exception,x:
        retmsg = '%s:%s' % (str(x),format_exc())
        print retmsg
    conn.close()
    
        

def main():
    test()
    
if __name__ == '__main__':
    main()
    
