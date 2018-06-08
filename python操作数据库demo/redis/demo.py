#coding=utf-8
import redis
import datetime
import time

def get_systime(strformat="%Y%m%d%H%M%s"):
    d = datetime.datetime.now()
    s = d.strftime(strformat)
    del d
    return s

def get_timelong():
    return int(time.time())

def get_redis_conn(host='127.0.0.1', port=6379, db=0):
    return redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def get_filecontent(fname=None):
    fin = open(fname)
    c = fin.read()
    fin.close()
    return c

def demo1():
    r = get_redis_conn()
    print r.ping()
    print "__file__:", __file__
    print "__name__:", __name__
    print "__lineno__:", __lineno__
    
def main():
    demo1()
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    