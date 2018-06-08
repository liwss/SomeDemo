# coding=gbk
# liupengc
import os
import time
import cx_Oracle

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
        self.fhandle.write("->")
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
#export BOSSCONFIG=/crmpdng/appnghcai/Eai/work/lpc/bossconfig.cfg
#boss_config_section:WCRMA1_DBCUSTOPR

def get_dbconn(boss_config_section):
    ## liupengc need modify;
    flag = 0 # liupengc for tmp test
    if flag == 1:
        decrypt_pro = "/appesb1/DataSynchronous/all/pass/dbdecrypt "
        get_dbinfo_srv = '%s %s %s' % (decrypt_pro, boss_config_section, '0')
        get_dbinfo_user = '%s %s %s' % (decrypt_pro, boss_config_section, '1')
        get_dbinfo_pwd = '%s %s %s' % (decrypt_pro, boss_config_section, '2')  
        
        p_pipe = os.popen(get_dbinfo_srv)
        dbsrv = p_pipe.read()
        p_pipe.close()

        p_pipe = os.popen(get_dbinfo_user)
        dbuser = p_pipe.read()
        p_pipe.close()

        p_pipe = os.popen(get_dbinfo_pwd)
        dbpwd = p_pipe.read()
        p_pipe.close()
        
        dbconn_str = '%s/%s@%s' % (dbuser, dbpwd, dbsrv)
        return dbconn_str
    else:
        return boss_config_section

#校验某个程序是否启动
def check_pro_exists(command_str):
    cmd_str = "ps -ef | grep -v grep | grep -v tail | grep -v vi | grep %s | wc -l" %  command_str
    p_pipe = os.popen(cmd_str)
    has_exists = p_pipe.read()
    p_pipe.close()
    print "cmd_str:", cmd_str
    print "has_exists:", has_exists
    return int(has_exists)
    
def db_opt(db_syn_section):
    sel_str = '''SELECT syn_id,
       src_db_section,
       dst_db_section,
       src_tab_owner,
       src_tab,
       dst_tab_owner,
       dst_tab,
       state,
       last_syn_time,
       now_syn_time,
       next_syn_time,
       syn_cycle,
       BAK_1, length(BAK_1)
       FROM t_syn_all
       WHERE state = '1' AND SYSDATE > now_syn_time '''
    #print sel_str
    up_str = '''UPDATE t_syn_all
       SET last_syn_time = SYSDATE, now_syn_time = sysdate + :v1
       WHERE syn_id = :v2'''
    up_str_month = '''UPDATE t_syn_all
       SET last_syn_time = SYSDATE, now_syn_time = add_months(sysdate,:v1)
       WHERE syn_id = :v2'''
    #print up_str
    #liupengc need modify 
    syn_all_py = " ./syn_all_new.py "
    mylog = Log('db_syn_all')
    dbcon_flag = 0
    dbcur_flag = 0
    dbcon = ''
    dbcur_sel = ''
    dbcur_up = ''
    while 1:
        try:
            if dbcon_flag !=1 :
                dbcon = cx_Oracle.connect(get_dbconn(db_syn_section))
                dbcon_flag = 1
                dbcur_sel = dbcon.cursor()
                dbcur_sel.prepare(sel_str)
                dbcur_up = dbcon.cursor()
                dbcur_up_mm = dbcon.cursor()
                dbcur_up.prepare(up_str)
                dbcur_up_mm.prepare(up_str_month)
                dbcur_flag = 1
            dbcur_sel.execute(None)
            rows = dbcur_sel.fetchall()
            for r in rows:
                if r[13] > 1:
                    tmp_tbl = r[12]
                else:
                    tmp_tbl = 'a'
                
                run_syn_cmd = 'nohup python %s %s %s %s %s %s %s %s %s > /dev/null 2>&1 &' % (syn_all_py, get_dbconn(r[1]), get_dbconn(r[2]), r[3], r[4], r[5], r[6], r[0], tmp_tbl  )
                print run_syn_cmd
                tmp_str = "'%s %s %s %s %s %s %s %s'" % ( get_dbconn(r[1]), get_dbconn(r[2]), r[3], r[4], r[5], r[6], r[0], tmp_tbl)
                print tmp_str
                has_exists = check_pro_exists(tmp_str)
                print has_exists
                cycle = 0
                if has_exists > 0:
                    mylog.debug(tmp_str + " 上一次计划没有执行完毕, 延迟5分钟后执行!\n")
                    cycle = float(5.0/60) * 1.0 / 24
                else:
                    mylog.debug(run_syn_cmd)                
                    cycle = float(r[11]) * 1.0 / 24
                os.system(run_syn_cmd)
                
                if cycle < 30: #对于大于30的按照, 一个月同步一次
                    dbcur_up.execute(None,[cycle,r[0],])
                else:
                    dbcur_up_mm.execute(None,[1,r[0],])
                dbcon.commit()
            time.sleep(3)
            print 'nodta find sleeping'
        except Exception,x:
            error, = x.args
            print("####### Operation exception: ",x)
            print error.code, error.message
            mylog.error(error.message)
            if dbcur_flag == 1:
                dbcur_up_mm.close()
                dbcur_up.close()
                dbcur_sel.close()
                dbcur_flag = 0
            if dbcon_flag == 1:
                dbcon.rollback()
                dbcon.close()
                dbcon_flag = 0
            time.sleep(1)
            continue    
            
                
        
def main():
    #print get_dbconn('WCRMA1_DBCUSTOPR')
    # sx offon bossconfig sqlplus OFFON/abc1234@SRVDB1
    #db_opt('APPINT_SRVDB1_OFFON')
    db_opt('liupeng/liupeng@liupeng')
    
if __name__ == '__main__':
    main()



