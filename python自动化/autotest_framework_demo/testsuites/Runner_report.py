# coding=utf-8
import os
import time
import unittest
from tools import HTMLTestRunner

#设置报告文件保存路径
report_path = os.path.dirname(os.path.abspath('.')) + '\\testreport\\'
#获取系统当前时间
now = time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time()))

#设置报告名称格式
htmlfile = report_path + now + "result.html"
fp = file(htmlfile,"wb")

# 构建suite
suite = unittest.TestLoader().discover("testsuites")

if __name__ == '__main__':
    #初始化一个HTMLTestRunner实例对象，用来生成报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"XXX项目测试报告", description=u"用例测试情况")
    #开始执行测试套件
    runner.run(suite)

