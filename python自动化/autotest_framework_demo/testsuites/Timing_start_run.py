# coding=utf-8
import os,time

k=1
while k<2:
    now_time=time.strftime("%H_%M")
    if now_time=="10_11":
        print "start to runscript!"
        os.system("Runner_report.py")
        print "Finished and exit!"
        break   #若想每天定时执行，则去掉break
    else:
        time.sleep(10)
        print now_time