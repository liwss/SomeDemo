# coding=utf-8
from framework.base_page import BasePage

class BaiduNewsHome(BasePage):
    radio1 = "id=>news"
    radio2 = "id=>newstitle"
    search_text = "id=>ww"
    search_button = "xpath=>//*/input[@class='btn']"
    sports_link = "xpath=>//*/a[@href='/sports']"

    def news_search(self, text):
        self.type(self.search_text, text)

    def send_submit_btn(self):
        self.click(self.search_button)

    def click_sports(self):
        self.click(self.sports_link)
        self.sleep(3)