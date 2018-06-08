# coding=utf-8
import os
import time
import unittest
from testsuites.baidu_pom_multi import BaiduSearch
from testsuites.baidu_search_single import BaiduSearch1

"""
#使用addTest添加类里面的单个测试用例到suite中
suite = unittest.TestSuite()
suite.addTest(BaiduSearch('test_baidu_search')) 
suite.addTest(BaiduSearch('test_result_num'))
suite.addTest(BaiduSearch1('test_baidu_search1'))
"""

"""
#使用makeSuite一次性加载一个类里的所有测试用例（test开头的方法）到suite中
suite = unittest.TestSuite(unittest.makeSuite(BaiduSearch)) 
"""

#使用discover一次性加载整个包或文件夹下面的所有测试用例
suite = unittest.TestLoader().discover("testsuites")


if __name__ == '__main__':
    #执行用例
    runner = unittest.TextTestRunner()
    runner.run(suite)