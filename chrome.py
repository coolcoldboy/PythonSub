# coding = utf-8
import time

__author__ = 'zhwang.kevin'

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://hotel.fliggy.com/hotel_list3.htm?cityName=%B1%B1%BE%A9&city=&keywords=&checkIn=2017-10-16&checkOut=2017-10-17')
browser.maximize_window()
time.sleep(3)

browser.find_element_by_class_name('pi-pagination-next').click()
browser.find_element_by_id('J_List')







