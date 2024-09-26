# the class we inherit
from unittest import TestCase

# the webdriver module is for automating browsers
from selenium import webdriver

# the By class is for searching web elements By tag_name, id etc.
from selenium.webdriver.common.by import By

# with chrome Options class you can configure the browser (maximize
from selenium.webdriver.chrome.options import Options

# operating system - for current working directory
import os

#for sleep so you can see the test slowly
import time

class TestHome(TestCase):

    driver = None
    base_url = f'file://{os.getcwd()}/web/'
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


    def test_h1_text(self):
        self.driver.get(f'{self.base_url}home.html')
        h1 = self.driver.find_element(By.TAG_NAME, 'h1')
        expected_h1_text = 'Automation Project - Main Page'
        self.assertEqual(expected_h1_text ,h1.text)

    def testUrl(self):
        url = self.driver.current_url
        url ='aaa?bbb'
        parts = url.split('?')
        print(parts)