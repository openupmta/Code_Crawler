# -*- coding: utf-8 -*-
import datetime

import time
import logging
# from builtins import Exception
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from tqdm import tqdm
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from scrapy_selenium import SeleniumRequest

class Crawler(object):

    def __init__(self, chromedriver):
        self.logging = logging
        self.logging.basicConfig(filename='crawler.log', level=logging.INFO,
                                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #
        # self.planning = []
        # self.controller_port = ControllerPort()
        # self.controller_region = ControllerRegion()
        # self.controller_vessel = ControllerVessel()
        # self.controller_load_planning = ControllerLoadPlanning()
        # self.controller_vehicle = ControllerVehicle()
        self.chromdriver = chromedriver

    def _connect_to_website(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        # Optional argument, if not specified will search path.
        # print(self.chromdriver)
        logging.info(self.chromdriver)
        self.driver = webdriver.Chrome(self.chromdriver, chrome_options=chrome_options)
        self.driver.get("https://batdongsan.com.vn/nha-dat-ban")
        # self.username = 'FH_Steyr'
        # self.password = '§HS_Steyr_2019_BMW'
        #
        # # self.port_of_loading =
        # self.refresh_btn = '/html/body/form/table/tbody/tr[1]/td[3]/input'
        self.timeout = 20

    def login(self):
        username_xpath = '/html/body/div/form/table/tbody/tr[2]/td[2]/input'
        password_xpath = '/html/body/div/form/table/tbody/tr[3]/td[2]/input'
        submit_btn_xpath = '/html/body/div/form/table/tbody/tr[5]/td[2]/input'
        status = self.input_text(username_xpath, self.username)
        assert status is True
        status = self.input_text(password_xpath, self.password)
        assert status is True
        status = self.click_element(submit_btn_xpath)
        assert status is True

        self.driver.get('https://www.afg.de/language/DEU/scripts/cgiip.exe/WService=WS_aspint/Schiffsplanung4.w')

    def click_element(self, xpath):
        """
        Given xpath of button, find and click the button
        :param xpath:
        :return:
        """
        button = self.driver.find_element_by_xpath(xpath)
        if button:
            button.click()
            return True
        return False

    def input_text(self, xpath, text):
        """
        Find element and send text to box
        :param xpath:
        :param text:
        :return:
        """
        elem = self.driver.find_element_by_xpath(xpath)
        if elem:
            elem.send_keys(text)
            return True
        return False

    def get_text(self, xpath):
        """
        Given xpath, return text contain in html element
        :param xpath:
        :return:
        """
        elem = self.driver.find_element_by_xpath(xpath)
        return elem.text if elem else ''

    def select_dropdown(self, xpath_dropdown, xpath_choose):
        """
        :param xpath_dropdown:
        :param xpath_choose:
        :code : v1: Type SECLECT OPTION
                      v2: Click is not SELECT OPTION
        :return:
        """
        try:
            # v1
            # element_present = EC.presence_of_element_located((By.XPATH, xpath))
            # WebDriverWait(self.driver, self.timeout).until(element_present)
            # select = Select(self.driver.find_element_by_xpath(xpath))
            #
            # # select by visible text
            # select.select_by_visible_text(value)
            # v2
            element_present = EC.element_to_be_clickable((By.XPATH, xpath_dropdown))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            self.click_element(xpath_dropdown)
            self.click_element(xpath_choose)

        except Exception as ex:
            print(ex.__str__())

        # select by value
        # select.select_by_value('1')

    def start_crawler(self):
        logging.info('=========Start Crawler==========')
        logging.info('Time: %s', datetime.datetime.today())
        try:
            self._connect_to_website()

            # Click choose "Loai nhà đất"
            self.select_dropdown('//div[@class="search-bar shadow-lv-1 clearfix"]/div[@id="divCategoryRe"]',
                                 '//*[@id="divCate"]/ul/li[1]')
            # Click choose "Khu vực"
            self.select_dropdown('//*[@id="boxSearchForm"]/div/div[4]/div[1]','//*[@id="mCSB_4_container"]/ul/li[1]')
            # Click choose "Mức giá"
            self.select_dropdown('//*[@id="boxSearchForm"]/div/div[5]/div[1]','//*[@id="mCSB_5_container"]/ul/li[1]')
            # Click "Tìm kiếm"
            self.click_element('//*[@id="btnSearch"]')
            current_url = self.driver.current_url()


        except Exception as e:
            print(e.__str__())

    def close_driver(self):
        self.driver.close()
        logging.info('===== Close Connect =====')


def start(chromedriver):
    # save_port()
    worker = Crawler(chromedriver=chromedriver)

    worker.start_crawler()
    worker.close_driver()
