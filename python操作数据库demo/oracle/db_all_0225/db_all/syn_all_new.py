#!env python
# -*- coding: gbk -*-

# liupengc 全量表数据复制
# 从A库同步到B库
# 要求同步的俩个表的表结构完全相同
# 启动参数描述:
# python syn_all_new.py 源库连接串 目标库连接串 源库表的属主名 源库表名 目标库表的属主名 目标库表名 同步的编号 目标库临时表名
# 其中 如果没有临时表的话,需要传入一个英文字母.


import sys
import os
import cx_Oracle
import time

import linecache



class Log:
    def __init__(self, fname):
        self.fname = fname
        self.dd = time.strftime("%Y%m%d")
        self.logdir = '%s/log' % os.getcwd()
        if not os.access(self.logdir,os.R_OK):
            os.mkdir(self.logdir)
        self.fhandle = file("%s/%s.%s.log"%(self.logdir,self.fname, self.dd), "a")

    def write(self, tag, msg):
        dd = time.strftime("%Y%m%d")
        tt = time.strftime("%Y%m%d%H%M%S")
        if self.dd != dd:
            self.fhandle.close()
            self.dd = dd
            self.fhandle = file("%s/%s.%s.log"%(self.logdir,self.fname, self.dd), "a")
        self.fhandle.write(tt)
        self.fhandle.write("|")
        self.fhandle.write(tag)
        self.fhandle.write(msg)
        self.fhandle.write('\n')
        self.fhandle.flush()

    def info(self, msg):
        self.write('INFO ', msg)
    def warn(self, msg):
        self.write('WARN ', msg)
    def debug(self, msg):
        self.write('DEBG ', msg)
    def fatal(self, msg):
        self.write('FATL ', msg)
    def error(self, msg):
        self.write('ERRO ', msg)
    def close(self):
        self.fhandle.close()

test_len = 2
        
# 设置初始值,可以在数据库出错的情况下,重新设置这个值.     
lob_default_size = 512000
def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, lob_default_size, cursor.arraysize)
    if defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, lob_default_size, cursor.arraysize)


def printStack(fout=sys.stdout):
    #这个方法是打印错误堆栈信息的
    ttype, value, tb = sys.exc_info()
    if ttype is None:
        fout.write('NoCurrentExceptionError\n')
        return
    stackOffset = 1
    frames = []
    while tb is not None:
        f = tb.tb_frame
        localz = f.f_locals.copy()
        if f.f_locals is f.f_globals:
            globalz = {}
        else:
            globalz = f.f_globals.copy()
        for d in globalz, localz:
            if d.has_key("__builtins__"):
                del d["__builtins__"]

        frames.append([
            f.f_code.co_name,
            f.f_code.co_filename,
            tb.tb_lineno,
            localz.items(),
            globalz.items(),
            ])
        tb = tb.tb_next
    w = fout.write
    w( 'Traceback (most recent call last):\n')
    for method, filename, lineno, localVars, globalVars in frames:
        w( '  File "%s", line %s, in %s\n' % (filename, lineno, method))
        w( '    %s\n' % linecache.getline(filename, lineno).strip())

# tmptbl 在目的数据库中创建的临时数据库表名
def get_sql(src_co, src_owner, src_table, dst_owner, dst_table, tmptbl):
    '根据表结构生成 select 和 insert 语句'
    cur = src_co.cursor()
    cur.execute("""select COLUMN_NAME, DATA_TYPE, NULLABLE 
        from all_tab_columns
        where table_name=:tname and owner=:owner order by COLUMN_ID""",
        tname=src_table.upper(), owner=src_owner.upper())

    cols_sel = []
    ins1 = []
    ins2 = []
    setinputsizes_paras = []
    col_inx = {}
    col_type = {}
    i = 0
    for r in cur.fetchall():
        col_inx[r[0]] = i
        ins1.append(r[0])
        cols_sel.append(r[0])
        ins2.append(":v%d"%i)
        if r[1] ==  'NUMBER':
            setinputsizes_paras.append(cx_Oracle.NUMBER)
        elif r[1] ==  'CHAR':
            setinputsizes_paras.append(cx_Oracle.FIXED_CHAR)
        elif r[1] ==  'VARCHAR2':
            setinputsizes_paras.append(cx_Oracle.STRING)
        elif r[1] ==  'CLOB':
            setinputsizes_paras.append(cx_Oracle.LONG_STRING)
        elif r[1] ==  'BLOB':
            setinputsizes_paras.append(cx_Oracle.LONG_BINARY)
        elif r[1] ==  'DATE':
            setinputsizes_paras.append(cx_Oracle.DATETIME)
        else:
             setinputsizes_paras.append(cx_Oracle.STRING)
        col_type[r[0]] = setinputsizes_paras[i]
        i = i + 1
        
    sel_sql = "SELECT " + ",".join(cols_sel) + " FROM " + src_owner+ "." + src_table + " "
    if len(tmptbl)>2: # 如果需要使用临时表, 源表数据-->临时表-->目的表;
        ins_sql = "insert into " + dst_owner + "." + tmptbl + "(" + ",".join(ins1) + ") values(" + ",".join(ins2) + ")"
    else:
        ins_sql = "insert into " + dst_owner + "." + dst_table + "(" + ",".join(ins1) + ") values(" + ",".join(ins2) + ")"

    return sel_sql, ins_sql, setinputsizes_paras, col_inx, col_type
    

#   tran_data(src_co, dst_co, sel_sql, ins_sql,  dsttbl, tmptbl, 1,dst_tbl_name)
#def tran_data(src_co, dst_co, sel_sql, ins_sql, dsttbl=None, tmptbl=None,del_dst_data=None,dst_tbl_name=None ):
def  tran_data(src_co, dst_co, sel_sql, ins_sql, tmptbl, dsttbl, setinputsizes_paras):
    '数据传输'
    cur1 = src_co.cursor()
    cur1.execute(sel_sql)
    cur2 = dst_co.cursor()
    cur3 = dst_co.cursor()
    
    
    
    if len(tmptbl) > test_len:  #是否需要临时表, 空串表示不需要临时表, 如果需要临时表, 将临时表清空
        #try:
            #liupengc 临时表不再有程序创建, 由需要同步的目的库创建
            #cur2.execute("drop table "+tmptbl )
            cur3.execute("truncate table  " + tmptbl )
            dst_co.commit()
        #except:
        #    pass
        #cur2.execute("create table "+tmptbl+" as select * from "+dsttbl + " where 1=2")
        #dst_co.commit()
    else:
        cur3.execute("delete  " + dsttbl ) #暂不提交,等待到cur2执行完毕后再提交
    cur2.prepare(ins_sql)
    counter = 0
    commit_ct = 0
    while 1:
        rows = cur1.fetchmany(150)  #每次读出记录最多100条
        ct = len(rows)
        if ct == 0:
            break
        cur2.setinputsizes( *setinputsizes_paras )    
        cur2.executemany(None, rows)
        commit_ct += ct
        counter += ct
        #if commit_ct > 2000:  #每2000条提交一次
            #src_co.ping()
            #dst_co.ping()
        #    dst_co.commit()
        #    commit_ct = 0
    dst_co.commit()
    if len(tmptbl) > test_len: 
        cur2.execute("delete "+dsttbl)
        cur2.execute("insert into "+dsttbl + " select * from "+tmptbl)
        dst_co.commit()
    return counter

def usage():
    print 'python syn_all_tt.py src_db dst_db src_owner src_table dst_owner dst_table'
    print 'python sys_all_tt.py 源库连接串 目标库连接串 源库同步表的属主名 源库表名 目标库表的属主名 目标库表名 同步的编号 目标库临时表名'    
    exit(1)
if __name__ == '__main__':
    mylog = Log('syn_all_detail')
    
    if len(sys.argv) != 9:
        mylog.error('sys.argv != 9')
        usage()
        
    src_db = sys.argv[1]#src_db = 'dbcrmoper/dbcrmoper@DB'
    dst_db = sys.argv[2]#dst_db = 'dbcrmoper/dbcrmoper@CRMDB'
    src_owner = sys.argv[3]
    src_table = sys.argv[4]
    dst_owner = sys.argv[5]
    dst_table = sys.argv[6]
    syn_id = sys.argv[7]
    #temp_table_name = 'syn_tmp_%s' % dst_table # 不再使用临时表
    #temp_table_name = '%s_syntmp' % dst_table
    temp_table_name = sys.argv[8]
    tbl_list = (
        # src_owner  src_table   dst_owner   dst_table    temp_table_name
        (src_owner,src_table,dst_owner,dst_table,temp_table_name),
        #('dbengine', 't1', 'dbengine', 'tk1', None),
    )

    # end of config data

    
    #while 1:
    src_co = ""
    dst_co = ""
    try:
        src_co = cx_Oracle.connect(src_db)
        dst_co = cx_Oracle.connect(dst_db)
        src_co.outputtypehandler = OutputTypeHandler
        dst_co.outputtypehandler = OutputTypeHandler
    except Exception,x:
        print '####### Exception:',x
        mylog.error("####### Exception: SYN_ID:[" + syn_id +"]" + str(x) )
        quit()
    
    setinputsizes_paras = []
    col_inx = {}
    col_type = {}
    for rc in tbl_list:
        src_owner, src_table, dst_owner, dst_table, tmptbl = rc
        try:
            sel_sql, ins_sql, setinputsizes_paras, col_inx, col_type  = get_sql(src_co, src_owner, src_table, dst_owner, dst_table, tmptbl)
            print "sel_sql:", sel_sql
            print "ins_sql:", ins_sql
            print "setinputsizes_paras:", setinputsizes_paras
            print "col_inx:", col_inx
            print "col_type:", col_type
        except:
            printStack()
            continue
        #if tmptbl:  ## 如果使用临时表的话, 那么 dsttbl 重新赋值, 否则 dsttbl 为 None
        #    dsttbl = dst_owner + '.' + dst_table
        #else:
        #    dsttbl = None
        while 1:
            try:
                t1 = time.time()
                #del_dst_data = 1
                dst_tbl_name = dst_owner + '.' + dst_table
                counter = tran_data(src_co, dst_co, sel_sql, ins_sql,  tmptbl, dst_table, setinputsizes_paras)
                t2 = time.time()
            #except: liupengc
            except Exception,x:
                print '####### Exception:',x
                if repr(type(x))=="<class 'cx_Oracle.DatabaseError'>":
                    error, = x.args
                    if error.code==1406:   #lob_default_size is small
                        lob_default_size = lob_default_size * 3
                        src_co.outputtypehandler = OutputTypeHandler
                        continue
                        
                mylog.error("####### Exception: SYN_ID:[" + syn_id + "]" + str(x))
                dst_co.rollback()
                print 'data_tran failed', dst_table
                printStack()
            break
        print 'table replicate:', src_owner, src_table, '==>', dst_owner, dst_table, ', counter:', counter, ', take time(s):', t2-t1
        ttt=" "
        mylog.debug('table trans syn_id:[' +syn_id+"] "  + src_owner + ttt + src_table + ' ==> ' + dst_owner + ttt + dst_table + ' counter:[' + str(counter) + ']time(s):' + str(t2-t1) )
    #time.sleep(120)
    src_co.close()
    dst_co.close()
        
