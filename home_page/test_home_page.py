from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time

class TestHome(TestCase):

    driver = None
    base_url = f'file://{os.getcwd()}/../web/'
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_title(self):
        self.driver.get(f'{self.base_url}home.html')
        expected_title = 'Automation Project'
        title = self.driver.title
        self.assertEqual(expected_title, title)


    def test_h1(self):
        pass


