import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pyautogui
from PIL import Image
from urllib.parse import urlparse, parse_qs

# Configuration
class Config:
    BASE_URL = f'file://{os.getcwd()}/web/'
    HOME_PAGE_TITLE = 'Automation Project'
    NEXT_PAGE_TITLE = 'Next Page'
    HOME_PAGE_H1_TEXT = 'Automation Project - Main Page'
    EXPECTED_NAMES = ['John', 'Jane', 'Alice', 'Michael', 'Emily']
    SCREENSHOTS_DIR = 'screenshots'

# Base class for all tests
class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the webdriver and maximize the window
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        if not os.path.exists(Config.SCREENSHOTS_DIR):
            os.makedirs(Config.SCREENSHOTS_DIR)

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests
        cls.driver.quit()

    def setUp(self):
        # Navigate to the home page before each test
        self.driver.get(Config.BASE_URL + 'home.html')
        self.test_screenshots_dir = os.path.join(Config.SCREENSHOTS_DIR, self._testMethodName)
        if not os.path.exists(self.test_screenshots_dir):
            os.makedirs(self.test_screenshots_dir)

    def capture_element_screenshot(self, element, filename):
        # Capture a screenshot of a specific element
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        WebDriverWait(self.driver, 10).until(EC.visibility_of(element))
        element.screenshot(os.path.join(self.test_screenshots_dir, f"{filename}.png"))

    def capture_browser_url_screenshot(self, filename):
        # Capture a screenshot of the entire browser window
        time.sleep(2)  # Wait for the browser to settle
        screenshot = pyautogui.screenshot()
        full_screenshot_path = os.path.join(self.test_screenshots_dir, f"{filename}_full.png")
        screenshot.save(full_screenshot_path)

        # Crop the top portion of the screenshot (browser URL line)
        with Image.open(full_screenshot_path) as im:
            width, height = im.size
            crop_rectangle = (0, 70, width, 170)  # Adjusted to capture URL line
            cropped_im = im.crop(crop_rectangle)
            cropped_im.save(os.path.join(self.test_screenshots_dir, f"{filename}_cropped.png"))

    def capture_browser_title_screenshot(self, filename):
        # Capture a screenshot of the entire browser window
        time.sleep(2)  # Wait for the browser to settle
        screenshot = pyautogui.screenshot()
        full_screenshot_path = os.path.join(self.test_screenshots_dir, f"{filename}_full.png")
        screenshot.save(full_screenshot_path)

        # Crop the top portion of the screenshot (browser URL line)
        with Image.open(full_screenshot_path) as im:
            width, height = im.size
            crop_rectangle = (0, 0, width, 100)  # Adjusted to capture URL line
            cropped_im = im.crop(crop_rectangle)
            cropped_im.save(os.path.join(self.test_screenshots_dir, f"{filename}_cropped.png"))

# Tests for the home page
class TestHomePage(TestBase):

    def test_homepage_url(self):
        expected_url = "file:///C:/QA%20Workspace/Automation_Project_Ido/home_page/web/home.html"
        self.assertEqual(expected_url, self.driver.current_url, "URL is incorrect - navigation to next page failed")
        self.capture_browser_url_screenshot("01_next_page_url_check")
        time.sleep(2)  # Pause for explanation of URL check

    def test_homepage_title(self):
        # Check if the page title is correct
        self.assertEqual(Config.HOME_PAGE_TITLE, self.driver.title, "Page title is incorrect")
        self.capture_browser_title_screenshot("02_title_check")
        time.sleep(2)  # Pause for explanation

    def test_h1_text(self):
        # Check if the H1 text is correct
        h1_element = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(Config.HOME_PAGE_H1_TEXT, h1_element.text, "H1 text is incorrect")
        self.capture_element_screenshot(h1_element, "03_h1_text_check")
        time.sleep(2)  # Pause for explanation

    def test_only_single_h1(self):
        # Check if there's only one H1 tag
        h1_list = self.driver.find_elements(By.TAG_NAME, 'h1')
        self.assertEqual(1, len(h1_list), "There should be only one h1 tag")
        self.capture_element_screenshot(h1_list[0], "04_single_h1_check")
        time.sleep(2)  # Pause for explanation

# Tests for the tables on the page
class TestTables(TestBase):
    def test_for_only_two_tables(self):
        # Check if there are exactly two tables
        tables = self.driver.find_elements(By.CLASS_NAME, 'table-container')
        self.assertEqual(2, len(tables), "There should be exactly two tables")
        self.capture_element_screenshot(tables[0], "05_two_tables_check")
        self.capture_element_screenshot(tables[1], "06_two_tables_check")
        time.sleep(3)  # Pause for explanation

    def test_first_table_title(self):
        # Check the title of the first table
        first_table = self.driver.find_element(By.TAG_NAME, 'h2')
        self.assertEqual("Cities of the World", first_table.text, "First table title is incorrect")
        self.capture_element_screenshot(first_table, "07_first_table_title_check")
        time.sleep(3)  # Pause for explanation

    def test_second_table_title(self):
        # Check the title of the second table
        second_table = self.driver.find_elements(By.TAG_NAME, 'h2')[1]
        self.assertEqual("Student Details", second_table.text, "Second table title is incorrect")
        self.capture_element_screenshot(second_table, "08_second_table_title_check")
        time.sleep(3)  # Pause for explanation

    def test_rows_in_students_table(self):
        # Check the number of rows in the students table
        tables = self.driver.find_elements(By.CLASS_NAME, 'table-container')
        rows = tables[1].find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(5, len(rows)-1, "Student table should have 5 rows (excluding header)")
        self.capture_element_screenshot(tables[1], "09_student_table_rows_check")
        time.sleep(3)  # Pause for explanation

    def test_name_list(self):
        # Check if the student names match the expected list
        tables = self.driver.find_elements(By.CLASS_NAME, 'table-container')
        first_name_cells = tables[1].find_elements(By.XPATH, ".//tbody/tr/td[2]")
        first_names = [cell.text for cell in first_name_cells]
        self.assertEqual(Config.EXPECTED_NAMES, first_names, "Student names do not match expected list")
        self.capture_element_screenshot(tables[1], "10_student_names_check")
        time.sleep(3)  # Pause for explanation

# Tests for form filling
class TestFillForm(TestBase):
    def fill_form_ref(self):
        # Fill the form with predefined data
        self.driver.find_element(By.ID, "first-name").send_keys("Ido")
        self.driver.find_element(By.ID, "last-name").send_keys("Hatuell")
        select = Select(self.driver.find_element(By.ID, "city"))
        select.select_by_visible_text("Jerusalem")
        self.driver.find_element(By.ID, "email").send_keys("ido1456@gmail.com")
        self.driver.find_element(By.ID, "mobile").send_keys("123-45-678")
        self.driver.find_element(By.ID, "male").click()
        self.driver.find_element(By.ID, "math").click()
        self.driver.find_element(By.ID, "physics").click()
        time.sleep(3)  # Pause for explanation of form filling

    def test_fill_form(self):
        # Test form filling and submission
        self.fill_form_ref()
        form = self.driver.find_element(By.TAG_NAME, 'form')
        self.capture_element_screenshot(form, "11_form_filled")
        self.driver.find_element(By.ID, "submit-form").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('?'))
        self.capture_browser_url_screenshot("12_form_submitted")
        time.sleep(3)  # Pause for explanation of form submission

        current_url = self.driver.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # Check each form field in the URL query
        self.assertEqual("Ido", query_params.get('first-name', [''])[0])
        self.assertEqual("Hatuell", query_params.get('last-name', [''])[0])
        self.assertEqual("Jerusalem", query_params.get('city', [''])[0])
        self.assertEqual("ido1456@gmail.com", query_params.get('email', [''])[0])
        self.assertEqual("123-45-678", query_params.get('mobile', [''])[0])
        self.assertEqual("male", query_params.get('gender', [''])[0])
        self.assertIn("math", query_params.get('proffesions', []))
        self.assertIn("physics", query_params.get('proffesions', []))
        time.sleep(3)  # Pause for explanation of URL query check

    def test_clear_form(self):
        # Fill out the form first
        self.fill_form_ref()
        form = self.driver.find_element(By.TAG_NAME, 'form')
        self.capture_element_screenshot(form, "13_form_filled")

        time.sleep(3)
        # Clear the form using the reset button
        self.driver.find_element(By.ID, "reset-form").click()
        self.capture_element_screenshot(form, "14_form_cleared")


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


# Tests for the download functionality
# בדיקות פונקציונליות לכפתור ההורדה
class TestDownload(TestBase):
    def test_download_button(self):
        # Test if clicking the download button starts the download process
        fieldset_element = self.driver.find_element(By.XPATH,"//fieldset[legend[contains(text(), 'Downloading Progress')]]")
        self.driver.find_element(By.XPATH, "//button[text()='Start Downloading']").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "download-progress"))
        )
        progress_bar = self.driver.find_element(By.ID, "download-progress")
        self.assertTrue(progress_bar.is_displayed(), "Progress bar not displayed after clicking download")
        self.capture_element_screenshot(fieldset_element, "15_download_started")
        time.sleep(3)  # Pause for explanation of download start

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "progress-txt"), "100")
        )
        progress_value = self.driver.find_element(By.ID, "download-progress").get_attribute("value")
        self.assertEqual("100", progress_value, "Download did not complete")
        self.capture_element_screenshot(fieldset_element, "16_download_completed")
        time.sleep(3)  # Pause for explanation of download completion

    def test_finished_message_and_dismissal(self):
        # Test if the finished message appears and can be dismissed
        fieldset_element = self.driver.find_element(By.XPATH,"//fieldset[legend[contains(text(), 'Downloading Progress')]]")

        self.driver.find_element(By.XPATH, "//button[text()='Start Downloading']").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "download-finished-msg"))
        )
        finished_msg = self.driver.find_element(By.ID, "download-finished-msg")
        self.assertTrue(finished_msg.is_displayed(), "Download finished message not displayed")
        self.capture_element_screenshot(finished_msg, "17_finished_message_displayed")
        time.sleep(3)  # Pause for explanation of finished message

        self.driver.find_element(By.XPATH, "//button[text()='OK']").click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "download-finished-msg"))
        )

        self.assertFalse(finished_msg.is_displayed(), "Download finished message still displayed after confirmation")
        self.capture_element_screenshot(fieldset_element, "18_finished_message_dismissed")
        time.sleep(3)  # Pause for explanation of message dismissal


# Tests for navigation
# בדיקות לניווט
class TestNavigation(TestBase):
    def test_next_page_url(self):
        # Test the URL change when navigating to the next page
        # Test navigation to the next page
        # בדיקת ניווט וכתובת URL לדף הבא
        self.driver.find_element(By.XPATH, "//a[text()='Next Page']").click()
        WebDriverWait(self.driver, 10).until(EC.title_is(Config.NEXT_PAGE_TITLE))
        expected_url = "file:///C:/QA%20Workspace/Automation_Project_Ido/home_page/web/nextpage.html"
        self.assertEqual(expected_url, self.driver.current_url, "URL is incorrect - navigation to next page failed")
        self.capture_browser_url_screenshot("19_next_page_url_check")
        time.sleep(3)  # Pause for explanation of URL check

    def test_next_page_title(self):
        # Check the title of the next page
        # בדיקת כותרת הדף הבא
        self.driver.find_element(By.XPATH, "//a[text()='Next Page']").click()
        WebDriverWait(self.driver, 10).until(EC.title_is(Config.NEXT_PAGE_TITLE))
        self.assertEqual(Config.NEXT_PAGE_TITLE, self.driver.title, "Page title is incorrect")
        self.capture_browser_title_screenshot("20_next_page_title_check")
        time.sleep(3)  # Pause for explanation of URL check

    # Check the title of the next page change
    # בדיקה לשינוי הכותרת בדף הבא
    def test_next_page_title_change(self):

        self.driver.find_element(By.XPATH, "//a[text()='Next Page']").click()
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Change Title']"))
        )
        self.driver.find_element(By.XPATH, "//button[text()='Change Title']").click()
        WebDriverWait(self.driver, 10).until(
            EC.title_is("Finish")
        )
        self.assertEqual("Finish", self.driver.title, "Title did not change")
        self.capture_browser_title_screenshot("21_next_page_title_change")

    def test_back_to_home_page(self):
        # Test the URL  when navigating back to the home page
        # בדיקת כתובת URL בעת חזרה לדף הבית

        time.sleep(3)
        self.driver.find_element(By.XPATH, "//a[text()='Next Page']").click()
        self.capture_browser_title_screenshot("22_back_to_home_page")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Back to Home Page']"))
        )
        self.driver.find_element(By.XPATH, "//a[text()='Back to Home Page']").click()
        time.sleep(2)

        expected_url = "file:///C:/QA%20Workspace/Automation_Project_Ido/home_page/web/home.html"
        self.assertEqual(expected_url, self.driver.current_url, "URL is incorrect - navigation to home page failed")
        self.capture_browser_title_screenshot("23_back_to_home_page")

if __name__ == "__main__":
    unittest.main()