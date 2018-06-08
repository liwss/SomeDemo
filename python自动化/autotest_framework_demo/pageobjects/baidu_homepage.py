# coding=utf-8
from framework.base_page import BasePage


class BaiduHomePage(BasePage):
    input_box = "id=>kw"
    search_submit_btn = "xpath=>//*[@id='su']"
    search_result_total = "xpath=>//*/div[@class='nums']"
    news_link = "xpath=>//*[@id='u1']/a[@name='tj_trnews']"

    def type_search(self, text):
        self.type(self.input_box, text)

    def send_submit_btn(self):
        self.click(self.search_submit_btn)

    def get_result_total(self):
        return self.find_element(self.search_result_total)

    def click_news(self):
        self.click(self.news_link)
        self.sleep(3)