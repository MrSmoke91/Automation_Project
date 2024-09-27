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

    # test for a single h1 tag in the code
    def test_only_single_h1(self):
        # getting access to the html file that contain the home page
        self.driver.get(f'{self.base_url}home.html')
        # searching and restoring in a variable a list of all the cases of h1 tags
        h1_list = self.driver.find_elements(By.TAG_NAME, 'h1')
        # the expected cases of h1 - 1
        expected_amount_of_h1 = 1
        # checking that there is only one element in the list
        self.assertEqual(expected_amount_of_h1, len(h1_list))

    def test_for_only_two_tables(self):
        # getting access to the html file that contain the home page
        self.driver.get(f'{self.base_url}home.html')
        # searching and restoring in a variable list of tables elements from the home page
        tables = self.driver.find_elements(By.CLASS_NAME, 'table-container')
        # the expected amount of tables
        expected_amount_of_tables = 2
        # checking that there are exactly two elements
        self.assertEqual(expected_amount_of_tables, len(tables))

    def test_first_table_title(self):
        # getting access to the html file that contain the home page
        self.driver.get(f'{self.base_url}home.html')
        # searching and restoring in a variable the first table element from the home page
        first_table = self.driver.find_element(By.TAG_NAME, 'h2')
        # the expected title of the first table
        expected_table_title = 'Cities of the World'
        # checking that the first table's title is 'Cities of the World'
        self.assertEqual(expected_table_title, first_table.text)

    def test_second_table_title(self):
        # getting access to the html file that contain the home page
        self.driver.get(f'{self.base_url}home.html')
        # searching and restoring in a variable the first table element from the home page
        second_table = self.driver.find_elements(By.TAG_NAME, 'h2')[1]
        # the expected title of the second table
        expected_table_title = 'Student Details'
        # checking that the second table's title is 'Student Details'
        self.assertEqual(expected_table_title, second_table.text)

    def test_row_in_students_table(self):
        # getting access to the html file that contain the home page
        self.driver.get(f'{self.base_url}home.html')
        # searching and restoring in a variable list of tables elements from the home page
        tables = self.driver.find_elements(By.CLASS_NAME, 'table-container')[1]
        # searching for all the rows in the table
        rows = tables.find_elements(By.TAG_NAME, 'tr')
        # getting the amount of rows - not counting the first row in a table - used for headlines
        rows_count = len(rows)-1
        # expected amount of rows
        expected_rows_count = 5
        # checking that there are 5 rows in the table
        self.assertEqual(expected_rows_count, rows_count)

    def test_name_list(self):
        pass

    def test_download_button(self):
        pass