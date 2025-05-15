import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    def _login(self):
        # Get the email from the .env file
        email = self._get_email()
        # Get the password from the .env file
        password = self._get_password()

        # Set up Chrome options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Set up the Chrome WebDriver
        self.driver = webdriver.Firefox(options=firefox_options)

        # Open a webpage
        self.driver.get("https://jinn.page/th/@SatitChula/home")

        # get a that href="https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14"
        student_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//a[@href='https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14']")
            )
        )

        # Click the button
        student_button.click()

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

        # Click the login button
        login_button.click()

        # wait until login button disappear
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//button[@class='btn btn-primary form-control']")
            )
        )

        self.driver.refresh()

        # button that text = "ลงทะเบียนวิชาเพิ่มเติม" #section2 > div.row.col-12.g-0.p-1.m-0.mb-5 > div:nth-child(5) > button
        register_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[.//small[contains(text(), 'ลงทะเบียนวิชาเพิ่มเติม')]"
                 " and contains(@class, 'btn-block')"
                 " and contains(@class, 'btn-secondary')]"
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
        self.driver = None
        self._login()

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
                            print("found subject name: ", subject_name)
                            print("found subject code: ", subject_code)
                            print("found subject section: ", section)
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
                continue

            if is_found:
                break