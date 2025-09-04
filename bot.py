import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options


class Subject:
    def __init__(self, name, code, section):
        self.name = name
        self.code = code
        self.section = section


class BotWorker:
    @staticmethod
    def _get_email():
        # load from file .env
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('email='):
                    return line.split('=')[1].strip()
        return None

    @staticmethod
    def _get_password():
        # load from file .env
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('password='):
                    return line.split('=')[1].strip()
        return None

    def login(self):
        # Open a webpage
        self.driver.set_page_load_timeout(6)

        is_success = False
        for i in range(5):
            try:
                self.driver.get("https://jinn.page/th/@SatitChula/home")
                is_success = True
                break
            except Exception as _:
                pass

        self.driver.set_page_load_timeout(90)
        if not is_success:
            self.driver.get("https://jinn.page/th/@SatitChula/home")

        # Get the email from the .env file
        email = self._get_email()
        # Get the password from the .env file
        password = self._get_password()

        for i in range(3):
            try:
                # get a that href="https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14"
                student_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//a[@href='https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14']")
                    )
                )

                # Click the button
                student_button.click()
                break
            except Exception as _:
                time.sleep(1)
                print("Retrying to find student button...")

        # wait for class swal2-confirm swal2-styled and text = "OK"
        ok_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[contains(@class, 'swal2-confirm') and contains(@class, 'swal2-styled') and text()='OK']")
            )
        )

        # Click the OK button if needed
        ok_button.click()

        # email input
        email_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "email-login-only")
            )
        )

        # Enter the email
        email_input.send_keys(email)
        # password input
        password_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "password")
            )
        )
        # Enter the password
        password_input.send_keys(password)

        # login button btn btn-primary form-control
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='btn btn-primary form-control']")
            )
        )
        time.sleep(1)

        for i in range(2):
            try:
                # Click the login button
                login_button.click()

                print("Logging in...")
                break
            except Exception as _:
                # wait for class swal2-confirm swal2-styled and text = "OK"
                try:
                    ok_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                             "//*[contains(@class, 'swal2-confirm') and contains(@class, 'swal2-styled') and text()='OK']")
                        )
                    )

                    # Click the OK button if needed
                    ok_button.click()
                except Exception:
                    pass
                time.sleep(1)
                print("Retrying login...")

        # wait until login button disappear
        for i in range(2):
            try:
                if i == 0:
                    timeout_second = 10
                else:
                    timeout_second = 5
                WebDriverWait(self.driver, timeout_second).until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, "//button[@class='btn btn-primary form-control']")
                    )
                )
            except Exception:
                pass
            self.driver.refresh()

        self.driver.refresh()

        # enter website button
        enter_website_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "/html/body/div/main/div[1]/div[1]/div/aside[2]/div/div[1]/button"
                 )
            )
        )
        enter_website_button.click()

        # element that contains text "ลงทะเบียนเลือกเพิ่มเติม 2/2568" (currently a div with inner <p>)
        register_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class,'hightlight-box-button')"
                 " or contains(@class,'highlight-box-button')]"
                 "[.//p[contains(normalize-space(.),'ลงทะเบียนเลือกเพิ่มเติม 2/2568')]]"
                 )
            )
        )
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=10)
        while datetime.datetime.now() < timeout:
            try:
                register_button.click()
                break
            except Exception as _:
                pass

    def __init__(self):
        # Set up Chrome options
        firefox_options = Options()
        # firefox_options.add_argument("--headless")  # ** MUST RUN IN HEADLESS MODE TO !!! **
        firefox_options.add_argument("--disable-gpu")  # keeps things stable on Windows

        # Set up Chrome options
        # chrome_options = webdriver.ChromeOptions()

        # Set up the Chrome WebDriver
        self.driver = webdriver.Firefox(options=firefox_options)

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()

    def refresh(self):
        # refresh the page
        self.driver.refresh()

    def enroll(self, subject: Subject):
        # zone header รายวิชา ที่สามารถเลือกได้ h6
        zone_header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[contains(text(), 'รายวิชา ที่สามารถเลือกได้')]")
            )
        )
        zone = zone_header.find_element(By.XPATH, "..").find_element(By.XPATH, "..")

        # print(table.get_attribute('outerHTML'))

        tables = zone.find_elements(By.XPATH, ".//table")

        subject_to_select_table = None
        header = []
        for table in tables:
            table_header = []
            # get all th
            th = table.find_elements(By.TAG_NAME, 'th')
            for i in th:
                table_header.append(i.text)

            if len(table_header) == 10 and table_header.__contains__("รายวิชา"):
                subject_to_select_table = table
                header = table_header
                break

        is_found = False
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=10)
        while datetime.datetime.now() < timeout:
            try:
                # find the row to click
                rows = None
                timeout = datetime.datetime.now() + datetime.timedelta(seconds=10)
                while datetime.datetime.now() < timeout:
                    rows = subject_to_select_table.find_elements(By.TAG_NAME, 'tr')
                    if len(rows) <= 1:
                        continue
                    else:
                        break

                for row in rows:
                    # get all td
                    tds = row.find_elements(By.TAG_NAME, 'td')
                    if len(tds) == 10:
                        # get the subject name
                        subject_name = tds[header.index("รายวิชา")].text.strip()
                        # get the subject code
                        subject_code = tds[header.index("รหัสวิชา")].text.strip()
                        # get the section
                        section = tds[header.index("กลุ่ม")].text.strip()

                        if subject_name == subject.name and subject_code == subject.code and section == subject.section:
                            print(
                                f"Found subject: {subject_name} ({subject_code}) section {section}")
                            is_found = True

                            # เลือก td
                            select_td = tds[header.index("เลือก")]
                            # try to click at every element inside that clickable include td itself
                            child_elements = select_td.find_elements(By.XPATH, ".//*")
                            for element in child_elements:
                                try:
                                    element.click()
                                except Exception:
                                    pass

            except Exception as e:
                # print(f"Error: {e}")
                continue

            if is_found:
                break
        if not is_found:
            raise Exception(f"Subject not found: {subject.name} ({subject.code}) section {subject.section}")
