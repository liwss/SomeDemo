#coding=utf-8

test_1 = "系统默认加载为 utf-8 编码"
if 1:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

test_2 = "字符串各种机制的转换"
if 1:
    print int('a',16)
    
#coding=utf-8
import os
import time
import datetime

#### 设置系统的默认编码方式 ####
import sys
print "raw sys.getdefaultencoding()",sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print "new sys.getdefaultencoding()",sys.getdefaultencoding()
################################


############# 获得文件的行号,文件名称 ###########
def get_filename_line_no():
    import inspect
    try :
        c=inspect.currentframe()
        print "c.f_code.co_filename=%s,c.f_lineno=%d" % (c.f_code.co_filename,c.f_lineno,)
    finally :
        del c


        
############# 打印函数调用的详细堆栈 statck 信息 #########
import linecache
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
        
        
############# 获取函数调用的详细堆栈 statck 信息 #########
import linecache
def get_stackinfo():
    #这个方法是打印错误堆栈信息的
    ttype, value, tb = sys.exc_info()
    if ttype is None:
        return ""
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
    w = []
    w.append( 'Traceback (most recent call last):')
    for method, filename, lineno, localVars, globalVars in frames:
        w.append( '  File "%s", line %s, in %s' % (filename, lineno, method))
        w.append( '    %s' % linecache.getline(filename, lineno).strip())
    del frames
    return "\n".join(w)

#### 测试打印异常,跟踪堆栈的情况
def test_printStack():
    try:
        raise KeyError
    except Exception,x:
        printStack()

#### 获得系统时间
def get_systime(strformat="%Y%m%d%H%M%s"):
    d = datetime.datetime.now()
    s = d.strftime(strformat)
    del d
    return s

#### 获得过去的时间
####  print i,get_lasttime(y=1,m=i,d=8) 会出现2月31号的情况;
#### 不要在生产中使用这个函数
def get_lasttime(y=0,m=0,d=0,s="%04d%02d%02d"):
    old_date = datetime.date.today() - datetime.timedelta(days=d)
    time_info = [old_date.year,old_date.month,old_date.day]
    #tlt = list(time.localtime())
    #print type(tlt),tlt
    flag =  time_info[1] - m
    if flag > 0:
        time_info[1] = flag
    else:
        a = flag - 12
        b = a / -12
        c = a % -12
        time_info[0] = time_info[0] - b
        if c == 0:
            time_info[1] =  12
        else:
            time_info[1] =  12 + c
    time_info[0] = time_info[0] - y
    #time_info = time.localtime()[1]-m or 12
    return s%(time_info[0],time_info[1],time_info[2])
 
### 清除昨天的日志
def clean_log():
    lastDate = datetime.date.today() - datetime.timedelta(days=1)
    cmdstr = "rm -rf *%u%02u%02u* " % (lastDate.year, lastDate.month, lastDate.day) 
    os.system(cmdstr) 
    

def small_test():
    a={}
    b={}
    a["name"] = "liupengc"
    b["name"] = "liupengc_b"
    a.update(b)
    print a,b
    
    from itertools import imap, izip
    for i in imap(pow,(2,3,10), (5,2,3)):
        print i
    mylist = map(pow,(2,3,10), (5,2,3)) # [32, 9, 1000]
    t={}
    t["id"]=1001
    t["name"]="liupengc"
#t = {"id":1001,"name":"liupengc"}
#execute_command('CONFIG GET', "port", "save",**t)
def execute_command(*args, **options):
    command_name = args[0]
    print "args:",args
    #print "type(*args)",type(*args)
    print "options:",options
    #print "type(**options):",type(**options)
    print "command_name:",command_name
    
def redis_test():
    import redis
    params = {'host': '192.168.0.111', 'port': 6379, 'db': 0}
    r = redis.StrictRedis(**params)
    r.ping()
    print r.connection_pool.connection_kwargs #
    #time.sleep(2)
    key1 = 'mylist1'
    key2 = 'mylist2'
    
    r.delete(key1,key2)
    mylen = 10
    data = [i  for i in range(mylen)]
    r.rpush(key1, *data)
    len1 = r.llen(key1)
    print r.lrange(key1,0,-1)
    print ">>>> blpop"
    for i in range(mylen+1):
        a= r.blpop([key1,], 3)
        print r.lrange(key1,0,-1),type(a)
        if a:
            print a[0],a[1]
    #print r.connection_pool.disconnect()
    
    
import sys
def get_cur_info():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return (f.f_code.co_name, f.f_lineno)

def callfunc():
    print get_cur_info()
    
    
def test1():
    import binascii
    a = binascii.b2a_hex('si-tech!')
    print a
    a = binascii.b2a_hex('''12345678''')
    print a
    
    Bob=('bob',30,'male')
    print 'Representation:',Bob
    Jane=('Jane',29,'female')
    print 'Field by index:',Jane[0]
    for people in [Bob,Jane]:
        print "%s is %d years old %s" % people


    
def main():
    print "liupengc"
    #get_filename_line_no()
    #test_printStack()
    #for i in range(25):
    #print get_lasttime(y=1,m=0,d=8+31)
    #small_test()
    #redis_test()
    t = {"id":1001,"name":"liupengc"}
    #execute_command('CONFIG GET', "port", "save",**t)
    callfunc()
if __name__ == '__main__':
    main()
    

####################################
#coding=utf8
__author__ = 'Administrator'

# 当函数的参数不确定时，
# 可以使用*args和**kwargs。
# *args没有key值，**kwargs有key值

def fun_var_args(farg, *args):
    print 'args:', farg
    for value in args:
        print 'another arg:',value

# *args可以当作可容纳多个变量组成的list或tuple
fun_var_args(1, 'two', 3, None)

#args: 1
#another arg: two
#another arg: 3
#another arg: None


def fun_var_kwargs(farg, **kwargs):
    print 'args:',farg
    for key in kwargs:
        print 'another keyword arg:%s:%s' % (key, kwargs[key])

# myarg1,myarg2和myarg3被视为key， 
# 感觉**kwargs可以当作容纳多个key和value的dictionary
fun_var_kwargs(1, myarg1='two', myarg2=3, myarg3=None)
# 输出：
#args: 1
#another keyword arg:myarg1:two
#another keyword arg:myarg2:3
#another keyword arg:myarg3:None

def fun_args(arg1, arg2, arg3):
    print 'arg1:', arg1
    print 'arg2:', arg2
    print 'arg3:', arg3

myargs = ['1', 'two', None]     # 定义列表
fun_args(*myargs)

# 输出：
#arg1: 1
#arg2: two
#arg3: None

mykwargs = {'arg1': '1', 'arg2': 'two', 'arg3': None}      # 定义字典类型
fun_args(**mykwargs)

# 输出：
#arg1: 1
#arg2: two
#arg3: None

# 两者都有
def fun_args_kwargs(*args, **kwargs):
    print 'args:', args
    print 'kwargs:', kwargs


args = [1, 2, 3, 4]
kwargs = {'name': 'BeginMan', 'age': 22}
fun_args_kwargs(args,kwargs)
# args: ([1, 2, 3, 4], {'age': 22, 'name': 'BeginMan'})
# kwargs: {}

fun_args_kwargs(1,2,3,a=100)
#args: (1, 2, 3)
#kwargs: {'a': 100}

fun_args_kwargs(*(1,2,3,4),**{'a':None})
#args: (1, 2, 3, 4)
#kwargs: {'a': None}


#### python 的 deep copy and shallow copy
http://www.cnblogs.com/BeginMan/p/3197649.html


#### 关于yield

def g():
   print 'step 1'
   x = yield 'hello'
   print 'step 2', 'x=', x
   y = 5 + (yield x)
   print 'step 3', 'y=', y
   yield 9999
   
f = g()
mv = f.next()
print "f.next() return:",mv

mv = f.send(222)
print "f.send(222) return:",mv

mv = f.send(99)
print "f.send(99) return:",mv

>>>>>>>
step 1
f.next() return: hello
step 2 x= 222
f.send(222) return: 222
step 3 y= 104
f.send(99) return: 9999


http://www.yeolar.com/note/2012/10/31/python-yield/

####### 列表推导式 ##########
multiples = [ i for i in range(30) if i
http://www.cnblogs.com/tkqasn/p/5977653.html


