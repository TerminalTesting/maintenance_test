#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
from selenium import webdriver



class MaintenanceTest(unittest.TestCase):
    
    HOST = 'http://nsk.%s/' % os.getenv('HOST')
    ID = os.getenv('ID')
    driver = webdriver.Firefox()

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""

        self.driver.get('%slogout/' % self.ADDRESS)
        self.driver.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def test_maintenance(self):
        """ Выполняет процедуру из браузера и парсит страницу на наличие ответа """
        correct = True # Test status: True - runs well, False - an error occurred
        self.driver.get('%slogin' % self.HOST)
        
        self.driver.find_element_by_id('username').send_keys(os.getenv('AUTH'))
        self.driver.find_element_by_id('password').send_keys(os.getenv('AUTHPASS'))
        self.driver.find_element_by_class_name('btn-primary').click()
        
        self.driver.get('%sterminal/maintenance/%s' % (self.HOST, self.ID))
        status = self.driver.find_elements_by_tag_name('div')[1]
        if '2' not in status.text:
            correct = False
            print 'Во время выполнения теста произошла ошибка, подробности можно посмотреть на скриншоте'
            print status.text
            
        self.driver.get_screenshot_as_file('screenshot.png')

        assert correct, (u'Maintenance was finished with error')
