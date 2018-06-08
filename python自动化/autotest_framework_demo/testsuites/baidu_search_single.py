# coding=utf-8
import time
import unittest
from framework.browser_engine import BrowserEngine

class BaiduSearch1(unittest.TestCase):

    def setUp(self):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        :return:
        """
        browse = BrowserEngine(self)
        self.driver = browse.open_browser(self)


    def tearDown(self):
        """
        测试结束后的操作，这里基本上都是关闭浏览器
        :return:
        """
        self.driver.quit()

    def test_baidu_search1(self):
        """
        这里一定要test开头，把测试逻辑代码封装到一个test开头的方法里。
        :return:
        """
        self.driver.find_element_by_id('kw1').send_keys('selenium1')
        self.driver.find_element_by_id('su').click()
        time.sleep(3)
        try:
            assert 'selenium1' in self.driver.title
            rslttxt = self.driver.find_element_by_xpath("//*/div[@class='nums']").text
            txtrt = rslttxt.split(u"约")[1]  # 第一次切割得到 xxxx个，[1]代表切割右边部分
            txtnum = txtrt.split(u"个")[0]  # 第二次切割，得到我们想要的数字 [0]代表切割参照参数的左边部分
            print u"baidu_search1 共搜索到 %s 个结果" % txtnum
        except Exception as e:
            print "!!! baidu_search1 Test Fail:",format(e)


#加上下面这段代码，才能在cmd窗口通过python baidu_search_single.py运行；在Pycharm里面右键运行加不加下面这段都行
if __name__ == '__main__':
    unittest.main()