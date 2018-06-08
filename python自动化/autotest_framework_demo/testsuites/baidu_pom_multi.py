# coding=utf-8
import time
import unittest
from framework.browser_engine import BrowserEngine
from pageobjects.baidu_homepage import BaiduHomePage

class BaiduSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #测试固件的setUpClass的代码，主要是测试的前提准备工作
        browse = BrowserEngine(cls)
        cls.driver = browse.open_browser(cls)

    @classmethod
    def tearDownClass(cls):
        #测试结束后的操作，这里基本上都是关闭浏览器
        cls.driver.quit()

    def test_baidu_search(self):
        #这里一定要test开头，把测试逻辑代码封装到一个test开头的方法里。
        homepage = BaiduHomePage(self.driver)
        homepage.type_search('selenium')  # 调用页面对象中的方法
        homepage.send_submit_btn()  # 调用页面对象类中的点击搜索按钮方法
        time.sleep(2)
        homepage.get_windows_img()  # 调用基类截图方法
        try:
            assert 'selenium' in homepage.get_page_title()  # 调用页面对象继承基类中的获取页面标题方法
            print ('baidu_search Test Pass.')
        except Exception as e:
            print ('baidu_search Test Fail.', format(e))

    def test_result_num(self):
        """
        这个方法也用test开头，用于获取搜索结果的数目
        :return:
        """
        homepage = BaiduHomePage(self.driver)
        rslt_total = homepage.get_result_total()
        rslttxt = rslt_total.text
        txtrt = rslttxt.split(u"约")[1]  # 第一次切割得到 xxxx个，[1]代表切割右边部分
        txtnum = txtrt.split(u"个")[0]  # 第二次切割，得到我们想要的数字 [0]代表切割参照参数的左边部分
        print u"baidu_search 共搜索到 %s 个结果" % txtnum


if __name__ == '__main__':
    unittest.main()