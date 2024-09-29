import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.webdriver.support.ui import Select




# Configuration
class Config:
    BASE_URL = f'file://{os.getcwd()}/web/'
    HOME_PAGE_TITLE = 'Automation Project'
    NEXT_PAGE_TITLE = 'Next Page'
    HOME_PAGE_H1_TEXT = 'Automation Project - Main Page'
    EXPECTED_NAMES = ['John', 'Jane', 'Alice', 'Michael', 'Emily']

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(self, by, value):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def click_element(self, by, value):
        element = self.find_element(by, value)
        element.click()

class HomePage(BasePage):
    def get_h1_text(self):
        return self.find_element(By.TAG_NAME, 'h1').text

    def get_tables(self):
        return self.find_elements(By.CLASS_NAME, 'table-container')

    def get_download_button(self):
        return self.find_element(By.XPATH, "//button[text()='Start Downloading']")

    def get_progress_bar(self):
        return self.find_element(By.ID, "download-progress")

    def get_progress_text(self):
        return self.find_element(By.ID, "progress-txt")

    def get_finished_message(self):
        return self.find_element(By.ID, "download-finished-msg")

    def get_ok_button(self):
        return self.find_element(By.XPATH, "//button[text()='OK']")

    def get_next_page_link(self):
        return self.find_element(By.XPATH, "//a[text()='Next Page']")

    def get_title_change_button(self):
        return self.find_element(By.XPATH, "//button[text()='Change Title']")

    def get_back_to_homepage_link(self):
        return self.find_element(By.XPATH, "//a[text()='Back to Home Page']")

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(Config.BASE_URL + 'home.html')
        self.home_page = HomePage(self.driver)

class TestHomePage(TestBase):
    def test_title(self):
        self.assertEqual(Config.HOME_PAGE_TITLE, self.driver.title, "Page title is incorrect")

    def test_h1_text(self):
        self.assertEqual(Config.HOME_PAGE_H1_TEXT, self.home_page.get_h1_text(), "H1 text is incorrect")

    def test_only_single_h1(self):
        h1_list = self.driver.find_elements(By.TAG_NAME, 'h1')
        self.assertEqual(1, len(h1_list), "There should be only one h1 tag")

class TestTables(TestBase):
    def test_for_only_two_tables(self):
        tables = self.home_page.get_tables()
        self.assertEqual(2, len(tables), "There should be exactly two tables")

    def test_first_table_title(self):
        first_table = self.driver.find_element(By.TAG_NAME, 'h2')
        self.assertEqual("Cities of the World", first_table.text, "First table title is incorrect")

    def test_second_table_title(self):
        second_table = self.driver.find_elements(By.TAG_NAME, 'h2')[1]
        self.assertEqual("Student Details", second_table.text, "Second table title is incorrect")

    def test_rows_in_students_table(self):
        tables = self.home_page.get_tables()
        rows = tables[1].find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(5, len(rows)-1, "Student table should have 5 rows (excluding header)")

    def test_name_list(self):
        tables = self.home_page.get_tables()
        first_name_cells = tables[1].find_elements(By.XPATH, ".//tbody/tr/td[2]")
        first_names = [cell.text for cell in first_name_cells]
        self.assertEqual(Config.EXPECTED_NAMES, first_names, "Student names do not match expected list")


class TestFillForm(TestBase):
    def test_fill_form(self):
        # Fill out the form
        self.driver.find_element(By.ID, "first-name").send_keys("Ido")
        self.driver.find_element(By.ID, "last-name").send_keys("Hatuell")
        select = Select(self.driver.find_element(By.ID, "city"))
        select.select_by_visible_text("Jerusalem")
        self.driver.find_element(By.ID, "email").send_keys("ido1456@gmail.com")
        self.driver.find_element(By.ID, "mobile").send_keys("123-45-678")
        self.driver.find_element(By.ID, "male").click()
        self.driver.find_element(By.ID, "math").click()
        self.driver.find_element(By.ID, "physics").click()

        time.sleep(5)

        # Submit the form
        self.driver.find_element(By.ID, "submit-form").click()

        # Check if the form was submitted successfully
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('?')  # Assuming the form submission adds query parameters to the URL
        )

    def test_clear_form(self):
        # Fill out the form first
        self.test_fill_form()
        time.sleep(5)
        # Clear the form using the reset button
        self.driver.find_element(By.ID, "reset-form").click()

        # Check if all fields are cleared
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value((By.ID, "first-name"), "")
        )
        self.assertEqual("", self.driver.find_element(By.ID, "first-name").get_attribute("value"))
        self.assertEqual("", self.driver.find_element(By.ID, "last-name").get_attribute("value"))
        self.assertEqual("", self.driver.find_element(By.ID, "email").get_attribute("value"))
        self.assertEqual("", self.driver.find_element(By.ID, "mobile").get_attribute("value"))
        self.assertFalse(self.driver.find_element(By.ID, "male").is_selected())
        self.assertFalse(self.driver.find_element(By.ID, "math").is_selected())
        self.assertFalse(self.driver.find_element(By.ID, "physics").is_selected())

    def test_check_form_query(self):
        # Fill out the form
        self.test_fill_form()

        # Get the current URL after form submission
        current_url = self.driver.current_url

        # Parse the query string
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # Check if the form data is in the query string
        self.assertEqual("Ido", query_params.get('first-name', [''])[0])
        self.assertEqual("Hatuell", query_params.get('last-name', [''])[0])
        self.assertEqual("Jerusalem", query_params.get('city', [''])[0])
        self.assertEqual("ido1456@gmail.com", query_params.get('email', [''])[0])
        self.assertEqual("123-45-678", query_params.get('mobile', [''])[0])
        self.assertEqual("male", query_params.get('gender', [''])[0])
        self.assertIn("math", query_params.get('proffesions', []))
        self.assertIn("physics", query_params.get('proffesions', []))




class TestDownload(TestBase):
    def test_download_button_starts_download(self):
        self.home_page.get_download_button().click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.home_page.get_progress_bar())
        )
        progress_bar = self.home_page.get_progress_bar()
        self.assertTrue(progress_bar.is_displayed(), "Progress bar not displayed after clicking download")

    def test_download_completes(self):
        self.home_page.get_download_button().click()
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element((By.ID, "progress-txt"), "100")
        )
        progress_value = self.home_page.get_progress_bar().get_attribute("value")
        self.assertEqual("100", progress_value, "Download did not complete")

    def test_finished_message_and_dismissal(self):
        self.home_page.get_download_button().click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "download-finished-msg"))
        )
        finished_msg = self.home_page.get_finished_message()
        self.assertTrue(finished_msg.is_displayed(), "Download finished message not displayed")

        self.home_page.get_ok_button().click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "download-finished-msg"))
        )
        self.assertFalse(finished_msg.is_displayed(), "Download finished message still displayed after confirmation")

class TestNavigation(TestBase):
    def test_next_page(self):
        self.home_page.get_next_page_link().click()
        WebDriverWait(self.driver, 10).until(
            EC.title_is(Config.NEXT_PAGE_TITLE)
        )
        self.assertEqual(Config.NEXT_PAGE_TITLE, self.driver.title, "Navigation to next page failed")

    def test_next_page_url(self):
        self.home_page.get_next_page_link().click()
        WebDriverWait(self.driver, 5).until(
            EC.url_contains('nextpage.html')
        )
        expected_url = "file:///C:/QA%20Workspace/Automation_Project_Ido/home_page/web/nextpage.html"
        self.assertEqual(expected_url, self.driver.current_url, "URL is incorrect")

    def test_next_page_title_change(self):
        self.home_page.get_next_page_link().click()
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located ((By.XPATH, "//button[text()='Change Title']"))
        )
        self.home_page.get_title_change_button().click()
        WebDriverWait(self.driver, 10).until(
            EC.title_is("Finish")
        )
        self.assertEqual("Finish", self.driver.title, "Title did not change")

    def test_navigate_back_to_main_page(self):
        self.home_page.get_next_page_link().click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located ((By.XPATH, "//a[text()='Back to Home Page']"))
        )
        self.home_page.get_back_to_homepage_link().click()
        WebDriverWait(self.driver, 10).until(
            EC.title_is(Config.HOME_PAGE_TITLE)
        )
        expected_url = "file:///C:/QA%20Workspace/Automation_Project_Ido/home_page/web/home.html"
        self.assertEqual(expected_url, self.driver.current_url, "URL is incorrect")


if __name__ == "__main__":
    unittest.main()